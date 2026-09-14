#!/usr/bin/env python3
"""Create the self-contained Mac download from an already guarded firmware image."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile
import markdown

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--firmware', required=True, type=Path)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'packages')
    args = parser.parse_args()
    if '-DEV-' in args.firmware.name:
        parser.error('Refusing a development image.')
    match = re.fullmatch(r'magic8-([0-9][0-9A-Za-z.-]*)-esp32c6-merged\.bin', args.firmware.name)
    if not match:
        parser.error('Expected a versioned ESP32-C6 merged firmware image.')
    if not re.fullmatch(r'[0-9a-f]{40}', args.source_commit):
        parser.error('The firmware source commit must be its full 40-character Git SHA.')
    if not args.firmware.is_file():
        parser.error('The firmware image is missing.')
    image = args.firmware.read_bytes()
    if not image:
        parser.error('The firmware image is empty.')
    if subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT,text=True).strip():
        parser.error('Refusing uncommitted installer files. Commit the exact package inputs first.')
    version = match.group(1)
    files = {}
    # Explicit allowlist: no repository history, private notes, or build tools.
    names = ['installer/Install Magic 8.command', 'THIRD_PARTY.md']
    for arch in ('arm64', 'amd64'):
        names += [f'installer/vendor/esptool-macos-{arch}/{name}' for name in ('esptool', 'LICENSE')]
    for name in names:
        path = ROOT/name
        if not path.is_file():
            parser.error(f'Required package file is missing: {name}')
        files[name] = path.read_bytes()
    body = markdown.markdown((ROOT/'docs/INSTALLATION.md').read_text(), extensions=['tables','fenced_code'])
    css = 'body{font:18px/1.6 -apple-system,BlinkMacSystemFont,sans-serif;max-width:760px;margin:48px auto;padding:0 24px;color:#172b42}h1,h2,h3{line-height:1.2}h2{margin-top:2em}a{color:#075ba6}li{margin:.6em 0}code{font-size:.9em;background:#f2f4f6;padding:2px 5px}table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:8px}blockquote{border-left:4px solid #ccc;margin-left:0;padding-left:18px}pre{white-space:pre-wrap}@media print{body{margin:0;font-size:12pt}}'
    files['START HERE.html'] = (f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Install Magic 8 firmware</title><style>{css}</style><main>{body}</main></html>').encode()
    files['dist/'+args.firmware.name] = image
    installer_commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    metadata = {'version': version, 'status': 'walkthrough-candidate', 'firmware_source_repository': 'adamjdavidson/magic8-device-firmware', 'firmware_source_commit': args.source_commit, 'firmware_file':args.firmware.name, 'firmware_sha256':hashlib.sha256(image).hexdigest(), 'installer_source_commit':installer_commit, 'esptool_version':'5.4.0'}
    files['release.json'] = (json.dumps(metadata,indent=2)+'\n').encode()
    files['SHA256SUMS'] = ''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n' for name,data in sorted(files.items())).encode()
    args.output.mkdir(parents=True,exist_ok=True)
    archive = args.output/f'Magic8-Firmware-{version}-mac.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo('Magic 8 Firmware/'+name, date_time=(2026,1,1,0,0,0))
            info.create_system=3
            mode=0o755 if name.endswith('.command') or name.endswith('/esptool') else 0o644
            info.external_attr=(0o100000|mode)<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data)
    checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{checksum}  {archive.name}\n')
    print(archive)
    print('SHA-256: '+checksum)

if __name__=='__main__':
    main()
