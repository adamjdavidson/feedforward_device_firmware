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
    names = ['installer/Install Magic 8.command', 'THIRD_PARTY.md', 'docs/videos/battery-installation.mp4']
    for arch in ('arm64', 'amd64'):
        names += [f'installer/vendor/esptool-macos-{arch}/{name}' for name in ('esptool', 'LICENSE')]
    names += [f'docs/images/{name}.jpg' for name in ('device-buttons','loose-battery','open-case','battery-connected','insulating-sheet','battery-insulated')]
    for name in names:
        path = ROOT/name
        if not path.is_file():
            parser.error(f'Required package file is missing: {name}')
        files[name] = path.read_bytes()
    css = (ROOT/'docs/guide.css').read_text()
    guides = [
        ('START HERE.html', 'README.md', 'Install Magic 8 firmware'),
        ('FIT BATTERY.html', 'docs/BATTERY.md', 'Fit the Magic 8 battery'),
    ]
    for output, source, title in guides:
        copy = (ROOT/source).read_text().split('<!-- maintainer-links -->')[0]
        copy = copy.replace('(docs/BATTERY.md)', '(FIT%20BATTERY.html)')
        copy = copy.replace('(../README.md)', '(START%20HERE.html)')
        if source.startswith('docs/'):
            copy = copy.replace('(images/', '(docs/images/')
            copy = copy.replace('(videos/', '(docs/videos/')
            copy = copy.replace('battery-installation.mp4?raw=true)', 'battery-installation.mp4)')
        body = markdown.markdown(copy, extensions=['tables','fenced_code','toc'])
        if source == 'docs/BATTERY.md':
            body = body.replace('<p><strong><a href="docs/videos/battery-installation.mp4">', '<video controls playsinline preload="metadata" src="docs/videos/battery-installation.mp4" aria-label="Battery installation video"></video>\n<p><strong><a href="docs/videos/battery-installation.mp4">')
        files[output] = (f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style><main>{body}</main></html>').encode()
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
