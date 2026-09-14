import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import hashlib

SOURCE = Path(__file__).resolve().parents[1]

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='Magic 8 test ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.installer = self.root / 'installer'
        self.installer.mkdir()
        self.script = self.installer / 'Install Magic 8.command'
        shutil.copy2(SOURCE / 'installer/Install Magic 8.command', self.script)
        (self.root / 'dist').mkdir()
        self.image = self.root / 'dist/magic8-0.2.1-esp32c6-merged.bin'
        self.image.write_bytes(b'firmware fixture')
        for arch in ('arm64', 'amd64'):
            tool = self.installer / f'vendor/esptool-macos-{arch}/esptool'
            tool.parent.mkdir(parents=True)
            # USB is the sole substituted boundary. Never touch attached hardware.
            tool.write_text('#!/bin/bash\n[ "$1 $2 $3 $4 $5 $6 $7 $8" = "--chip esp32c6 --baud 460800 --port /dev/cu.usbmodemTEST write-flash 0x0" ] || exit 97\n[ -f "$9" ] || exit 98\nprintf called > "$INSTALLER_TEST_MARKER"\nexit "${INSTALLER_TEST_RESULT:-0}"\n')
            tool.chmod(0o755)
        self.mock_bin=self.root/'os-tools'
        self.mock_bin.mkdir()
        find=self.mock_bin/'find'
        find.write_text('#!/bin/bash\n[ "$*" = "/dev -maxdepth 1 -name cu.usbmodem* -print" ] || exit 96\nprintf "%s" "$INSTALLER_TEST_PORTS"\n')
        find.chmod(0o755)
        self.manifest()

    def manifest(self):
        paths = [p for p in self.root.rglob('*') if p.is_file() and p.name != 'SHA256SUMS']
        (self.root / 'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(self.root)}\n' for p in sorted(paths)))

    def run_installer(self, status=0, ports='/dev/cu.usbmodemTEST\n'):
        env = dict(os.environ, INSTALLER_TEST_MARKER=str(self.root/'called'), INSTALLER_TEST_RESULT=str(status), INSTALLER_TEST_PORTS=ports, PATH=str(self.mock_bin)+os.pathsep+os.environ['PATH'])
        return subprocess.run(['bash', str(self.script)], cwd='/', env=env, input='', text=True, capture_output=True, timeout=10)

    def test_success_returns_zero_even_when_final_prompt_has_no_stdin(self):
        r = self.run_installer()
        self.assertEqual(r.returncode, 0, r.stdout+r.stderr)
        self.assertIn('PASS', r.stdout)
        self.assertTrue((self.root/'called').exists())

    def test_failed_write_returns_failure_and_never_says_pass(self):
        r = self.run_installer(2)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('FAILED', r.stdout)
        self.assertNotIn('PASS', r.stdout)

    def test_development_image_is_refused_before_usb_access(self):
        self.image.rename(self.image.with_name('magic8-0.2.1-DEV-esp32c6-merged.bin'))
        self.manifest()
        r = self.run_installer()
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.root/'called').exists())
        self.assertIn('development', r.stdout.lower())

    def test_two_images_are_refused_before_usb_access(self):
        self.image.with_name('magic8-0.2.2-esp32c6-merged.bin').write_bytes(b'other')
        self.manifest()
        r = self.run_installer()
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.root/'called').exists())

    def test_two_devices_are_refused_without_writing_either(self):
        r=self.run_installer(ports='/dev/cu.usbmodemONE\n/dev/cu.usbmodemTWO\n')
        self.assertNotEqual(r.returncode,0)
        self.assertFalse((self.root/'called').exists())
        self.assertIn('one device',r.stdout.lower())

    def test_no_device_is_refused_without_calling_the_write_tool(self):
        r=self.run_installer(ports='')
        self.assertNotEqual(r.returncode,0)
        self.assertFalse((self.root/'called').exists())
        self.assertIn('no device',r.stdout.lower())

    def test_damaged_firmware_is_refused_before_usb_access(self):
        self.image.write_bytes(b'corrupted')
        r = self.run_installer()
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.root/'called').exists())
        self.assertIn('checksum', r.stdout.lower())

    def test_missing_checksum_file_is_refused_before_usb_access(self):
        (self.root/'SHA256SUMS').unlink()
        r = self.run_installer()
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.root/'called').exists())

if __name__ == '__main__':
    unittest.main()
