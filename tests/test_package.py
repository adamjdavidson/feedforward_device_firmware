import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

SOURCE = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='Magic 8 package ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = self.root/'magic8-0.2.1-esp32c6-merged.bin'
        self.image.write_bytes(b'firmware fixture')
        self.output = self.root/'output'
        self.build_root = self.root/'source'
        shutil.copytree(SOURCE, self.build_root, ignore=shutil.ignore_patterns('.git', 'packages', '__pycache__', '.venv'))
        subprocess.run(['git','init','-q'],cwd=self.build_root,check=True)
        subprocess.run(['git','add','.'],cwd=self.build_root,check=True)
        subprocess.run(['git','-c','user.name=Package Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],cwd=self.build_root,check=True)

    def run_builder(self):
        return subprocess.run([sys.executable,str(self.build_root/'tools/package.py'), '--firmware',str(self.image),'--source-commit','a'*40,'--output',str(self.output)],capture_output=True,text=True)

    def test_download_contains_one_image_readable_guide_and_executable_installer(self):
        r = self.run_builder()
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        archives = list(self.output.glob('*.zip'))
        self.assertEqual(len(archives),1)
        with zipfile.ZipFile(archives[0]) as z:
            names = z.namelist()
            self.assertEqual(len([n for n in names if n.endswith('.bin')]),1)
            root='Magic 8 Firmware/'
            self.assertIn(root+'START HERE.html',names)
            self.assertIn(root+'SHA256SUMS',names)
            self.assertEqual(z.read(root+'dist/'+self.image.name),b'firmware fixture')
            self.assertTrue((z.getinfo(root+'installer/Install Magic 8.command').external_attr >> 16) & 0o111)
            metadata=json.loads(z.read(root+'release.json'))
            self.assertEqual(metadata['firmware_sha256'],hashlib.sha256(b'firmware fixture').hexdigest())
            self.assertEqual(metadata['firmware_source_commit'],'a'*40)
            # Validate every manifest entry against the actual archived bytes.
            for line in z.read(root+'SHA256SUMS').decode().splitlines():
                digest,name=line.split('  ',1)
                self.assertEqual(digest,hashlib.sha256(z.read(root+name)).hexdigest())
            self.assertFalse(any('/.git/' in n or '/tests/' in n for n in names))

    def test_development_image_cannot_be_packaged(self):
        target=self.image.with_name('magic8-0.2.1-DEV-esp32c6-merged.bin')
        self.image.rename(target); self.image=target
        r=self.run_builder()
        self.assertNotEqual(r.returncode,0)
        self.assertIn('development',r.stderr.lower())
        self.assertFalse(list(self.output.glob('*.zip')))

    def test_uncommitted_installer_cannot_be_attributed_to_head(self):
        with (self.build_root/'installer/Install Magic 8.command').open('a') as f:
            f.write('\n# changed since commit\n')
        r=self.run_builder()
        self.assertNotEqual(r.returncode,0)
        self.assertIn('uncommitted',r.stderr.lower())
        self.assertFalse(list(self.output.glob('*.zip')))

    def test_empty_firmware_cannot_be_packaged(self):
        self.image.write_bytes(b'')
        r=self.run_builder()
        self.assertNotEqual(r.returncode,0)
        self.assertIn('empty',r.stderr.lower())

if __name__=='__main__': unittest.main()
