#!/usr/bin/env python3
"""Audit publishable Git files without printing any suspected secret values.

This is a narrow repository guard, not a general secret scanner or legal review.
Only the two reviewed, original demo PNGs are permitted as binary assets.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = {'docs/images/banner.png', 'docs/images/showcase.png'}
TEXT_SUFFIXES = {'.md', '.py', '.yaml', '.yml', '.txt'}
ROOT_FILES = {'LICENSE', '.gitignore'}
PRIVATE_PARTS = {'original', 'extracted', 'romfs', 'exefs', 'firmware', 'keys',
                 'secrets', 'backups', 'translations', 'research', 'private'}
PATTERNS = {
    'private key block': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'GitHub credential': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b'),
    'API credential': re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b'),
    'hexadecimal key assignment': re.compile(r'(?im)^\s*[\w.-]*(?:key|secret)[\w.-]*\s*[:=]\s*[\x22\x27]?[a-f0-9]{32,}'),
    'personal absolute path': re.compile(r'(?:/(?:Users|home)/[^/\s]+/|[A-Z]:\\Users\\[^\\\s]+\\)'),
}


def inspect_file(name, data):
    errors = []
    path = Path(name)
    if any(part.lower() in PRIVATE_PARTS for part in path.parts):
        errors.append('private workspace directory')
    if name in IMAGES:
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            errors.append('approved image is not PNG')
        if len(data) > 12 * 1024 * 1024:
            errors.append('unexpectedly large demo image')
        return errors
    if name not in ROOT_FILES and path.suffix not in TEXT_SUFFIXES:
        errors.append('file type not permitted in this public skill')
        return errors
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return errors + ['non-UTF-8 material']
    if '\x00' in text:
        errors.append('binary data in a text file')
    if len(data) > 256 * 1024:
        errors.append('unexpectedly large text file')
    errors.extend(label for label, pattern in PATTERNS.items() if pattern.search(text))
    return errors


def main():
    result = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                            cwd=ROOT, check=True, stdout=subprocess.PIPE)
    names = sorted(set(n.decode('utf-8') for n in result.stdout.split(b'\x00') if n))
    failures = []
    for name in names:
        path = ROOT / name
        if path.is_symlink():
            failures.append((name, 'symlinks are not public package inputs'))
        elif not path.is_file():
            failures.append((name, 'missing/nonregular Git file'))
        else:
            failures.extend((name, reason) for reason in inspect_file(name, path.read_bytes()))
    for name, reason in failures:
        print(f'FAIL {name}: {reason}')
    if failures:
        return 1
    print(f'PASS: {len(names)} publishable files; allowlist and text-pattern checks passed.')
    print('Review image provenance and Git history separately; this is not a legal or exhaustive secret audit.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
