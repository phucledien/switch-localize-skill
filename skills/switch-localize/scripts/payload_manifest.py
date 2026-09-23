#!/usr/bin/env python3
"""Create/verify strict file-integrity manifests; never installs or selects assets."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def files_in(root):
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in dirs + files:
            path = base / name
            if path.is_symlink():
                raise ValueError(f'Symlink is not a release payload: {path.relative_to(root)}')
        for name in files:
            path = base / name
            if not path.is_file():
                raise ValueError(f'Non-regular payload file: {path.relative_to(root)}')
            result[path.relative_to(root).as_posix()] = path
    return result


def safe_path(root, value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Invalid manifest path')
    rel = PurePosixPath(value)
    if rel.is_absolute() or '..' in rel.parts or str(rel) != value or value == '.':
        raise ValueError(f'Unsafe manifest path: {value}')
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Manifest path crosses a symlink: {value}')
    if not current.resolve().is_relative_to(root):
        raise ValueError(f'Path leaves payload: {value}')
    return current


def create(args, root):
    output = args.output.resolve()
    if output.is_relative_to(root):
        raise ValueError('Manifest must be outside the payload directory')
    if args.output.exists() or args.output.is_symlink():
        raise ValueError('Manifest already exists; use a new output path')
    if not re.fullmatch(r'[0-9a-fA-F]{16}', args.title_id):
        raise ValueError('Title ID must be exactly 16 hexadecimal characters')
    if args.build_id and not re.fullmatch(r'[0-9a-fA-F]{64}', args.build_id):
        raise ValueError('NSO build ID must be exactly 64 hexadecimal characters')
    paths = files_in(root)
    if not paths:
        raise ValueError('Empty payload')
    rows = [{'path': key, 'bytes': path.stat().st_size, 'sha256': digest(path)}
            for key, path in sorted(paths.items())]
    report = {'schema_version': 1, 'application_id': args.title_id.upper(),
              'game_version': args.game_version, 'language': args.language,
              'executable_build_id': args.build_id.upper() if args.build_id else None,
              'verification_scope': 'File identity only; target metadata is supplied by the caller.',
              'file_count': len(rows), 'total_bytes': sum(r['bytes'] for r in rows), 'files': rows}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return {'created': str(output), 'files': len(rows), 'bytes': report['total_bytes']}


def verify(args, root):
    report = json.loads(args.manifest.read_text(encoding='utf-8'))
    if report.get('schema_version') != 1 or not isinstance(report.get('files'), list):
        raise ValueError('Unsupported manifest schema')
    rows, seen = report['files'], set()
    if not rows:
        raise ValueError('Empty manifest')
    for row in rows:
        path = safe_path(root, row['path'])
        if row['path'] in seen:
            raise ValueError(f'Duplicate manifest path: {row["path"]}')
        seen.add(row['path'])
        if type(row['bytes']) is not int or row['bytes'] < 0 or not re.fullmatch(r'[0-9a-f]{64}', row['sha256']):
            raise ValueError(f'Invalid size/hash: {row["path"]}')
        if not path.is_file() or path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            raise ValueError(f'Payload mismatch: {row["path"]}')
    if report.get('file_count') != len(rows) or report.get('total_bytes') != sum(r['bytes'] for r in rows):
        raise ValueError('Manifest totals are inconsistent')
    extras = sorted(set(files_in(root)) - seen)
    if extras and not args.allow_extra:
        raise ValueError(f'Unexpected payload files: {extras}')
    return {'verified_files': len(rows), 'extra_files': extras,
            'scope': 'File identity; no translation/compatibility/hardware claim'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('create')
    make.add_argument('root', type=Path)
    make.add_argument('--output', type=Path, required=True)
    make.add_argument('--title-id', required=True)
    make.add_argument('--game-version', required=True)
    make.add_argument('--language', required=True)
    make.add_argument('--build-id')
    check = commands.add_parser('verify')
    check.add_argument('root', type=Path)
    check.add_argument('--manifest', type=Path, required=True)
    check.add_argument('--allow-extra', action='store_true')
    args = parser.parse_args()
    try:
        if args.root.is_symlink():
            raise ValueError('Choose the real payload folder, not a symlink')
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError('Payload must be a directory')
        result = create(args, root) if args.command == 'create' else verify(args, root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
