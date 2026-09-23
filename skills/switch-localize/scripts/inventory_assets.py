#!/usr/bin/env python3
"""Read-only inventory of a selected extracted asset folder; stdlib only."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path


def inventory(root, include_hash=False):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Input must be a directory')
    rows, skipped = [], []
    counts = collections.Counter()
    for directory, dirs, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in list(dirs):
            if (base / name).is_symlink():
                skipped.append(str((base / name).relative_to(root)))
                dirs.remove(name)
        dirs.sort()
        for name in sorted(files):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink() or not path.is_file():
                skipped.append(rel)
                continue
            size = path.stat().st_size
            suffix = path.suffix.lower() or '(none)'
            counts[suffix] += 1
            row = {'path': rel, 'bytes': size, 'extension': suffix}
            with path.open('rb') as stream:
                head = stream.read(32)
                if head.startswith(b'UnityFS\0'):
                    row['signature'] = 'UnityFS bundle'
                elif head.startswith(b'NSO0'):
                    row['signature'] = 'Nintendo Switch NSO'
                elif head.startswith(b'\x89PNG\r\n\x1a\n'):
                    row['signature'] = 'PNG'
                elif head.startswith(b'\xaf\x1b\xb1\xfa'):
                    row['signature'] = 'IL2CPP metadata candidate'
                if include_hash:
                    stream.seek(0)
                    digest = hashlib.sha256()
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(chunk)
                    row['sha256'] = digest.hexdigest()
            rows.append(row)
    return {'file_count': len(rows), 'total_bytes': sum(r['bytes'] for r in rows),
            'extensions': dict(sorted(counts.items())), 'skipped_symlinks_or_special_files': skipped,
            'note': 'Signatures/extensions are clues, not proof of active game/language assets.',
            'files': sorted(rows, key=lambda r: r['path'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--hash', action='store_true', dest='include_hash')
    args = parser.parse_args()
    root, output = args.root.resolve(strict=True), args.output.resolve()
    if output.is_relative_to(root):
        parser.error('Write the report outside the input tree to avoid self-inclusion.')
    if args.output.exists() or args.output.is_symlink():
        parser.error('Report already exists; choose a new path or deliberately remove the old report.')
    report = inventory(root, args.include_hash)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'files'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
