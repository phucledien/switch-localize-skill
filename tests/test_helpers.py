"""Synthetic fixtures only; no game content or real secrets."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/switch-localize/scripts'
spec = importlib.util.spec_from_file_location('audit', ROOT / 'tools/audit_public.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class Helpers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.payload = self.base / 'payload'
        self.payload.mkdir()
        (self.payload / 'sample.txt').write_text('Original synthetic fixture.\n', encoding='utf-8')
        self.manifest = self.base / 'manifest.json'

    def run_script(self, name, *args, ok=True):
        p = subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(p.returncode == 0, ok, p.stderr)
        return p

    def create(self):
        return self.run_script('payload_manifest.py', 'create', self.payload, '--output', self.manifest,
                               '--title-id', '0123456789ABCDEF', '--game-version', 'synthetic', '--language', 'en')

    def verify(self, ok=True):
        return self.run_script('payload_manifest.py', 'verify', self.payload, '--manifest', self.manifest, ok=ok)

    def test_inventory_is_read_only_and_hashes(self):
        original = (self.payload / 'sample.txt').read_bytes()
        report = self.base / 'inventory.json'
        self.run_script('inventory_assets.py', self.payload, '--output', report, '--hash')
        j = json.loads(report.read_text())
        self.assertEqual(j['file_count'], 1)
        self.assertEqual(len(j['files'][0]['sha256']), 64)
        self.assertEqual((self.payload / 'sample.txt').read_bytes(), original)
        self.run_script('inventory_assets.py', self.payload, '--output', report, ok=False)
        self.run_script('inventory_assets.py', self.payload, '--output', self.payload / 'report.json', ok=False)

    def test_manifest_detects_tampering(self):
        self.create()
        self.verify()
        (self.payload / 'sample.txt').write_text('Tampered fixture.\n')
        self.verify(ok=False)

    def test_manifest_rejects_extra_file(self):
        self.create()
        (self.payload / 'unexpected.txt').write_text('extra')
        self.verify(ok=False)

    def test_manifest_rejects_traversal_and_duplicates(self):
        self.create()
        original = json.loads(self.manifest.read_text())
        j = json.loads(self.manifest.read_text())
        j['files'][0]['path'] = '../outside.txt'
        self.manifest.write_text(json.dumps(j))
        self.verify(ok=False)
        original['files'].append(original['files'][0].copy())
        self.manifest.write_text(json.dumps(original))
        self.verify(ok=False)

    def test_manifest_refuses_overwrite_and_symlink(self):
        self.create()
        self.run_script('payload_manifest.py', 'create', self.payload, '--output', self.manifest,
                        '--title-id', '0123456789ABCDEF', '--game-version', 'synthetic', '--language', 'en', ok=False)
        (self.payload / 'link.txt').symlink_to(self.payload / 'sample.txt')
        self.verify(ok=False)

    def test_inventory_skips_symlinks(self):
        (self.payload / 'link.txt').symlink_to(self.payload / 'sample.txt')
        out = self.base / 'inventory.json'
        self.run_script('inventory_assets.py', self.payload, '--output', out)
        j = json.loads(out.read_text())
        self.assertEqual(j['file_count'], 1)
        self.assertEqual(j['skipped_symlinks_or_special_files'], ['link.txt'])

    def test_public_guard_rejects_private_material(self):
        self.assertTrue(audit.inspect_file('game.nsp', b'fake container'))
        self.assertTrue(audit.inspect_file('extracted/source.txt', b'private data'))
        key_assignment = ('example_' + 'key = ' + 'a' * 32).encode()
        self.assertIn('hexadecimal key assignment', audit.inspect_file('notes.txt', key_assignment))
        self.assertTrue(audit.inspect_file('docs/images/unreviewed.png', b'fake image'))
        self.assertEqual(audit.inspect_file('docs/example.md', b'Original generic guidance.'), [])


if __name__ == '__main__':
    unittest.main()
