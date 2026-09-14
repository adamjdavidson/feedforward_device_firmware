# Mac firmware installer implementation plan

Goal: publish a public code repository and a self-contained Mac download for Adam's new-device walkthrough.

The firmware source stays in its existing repository. This repository owns installation and packaging. Recipients unzip the download, read START HERE.html, and double-click installer/Install Magic 8.command. No build tools, commands or downloads during installation.

- Prepare version 0.2.1 from a clean firmware checkout with release guards enabled. Merge its PR only after all five required checks and review comments are resolved.
- Copy the established Mac installer and bundled Apple Silicon/Intel esptool executables. Preserve upstream licenses.
- Exercise the installer with a controlled substitute for the USB-writing program: successful writes, failed writes, development images, ambiguous images, missing and corrupt checksums. Watch the new guards fail before implementing them.
- Generate the ZIP from an explicit file list. Include a readable HTML guide, one image and SHA-256 checksums; record source commit and firmware hash.
- Verify archive contents and executable permissions after extraction. Publish code through a PR with passing CI, then publish a clearly labeled walkthrough pre-release.
- Download the published asset through a browser. Inspect the actual first-launch behavior and walk the new device with Adam. Record observations; do not infer physical success from software checks.

Open charging durations and unobserved power-button behavior remain outside the verified procedure. The public guide marks battery assembly instructions as provisional and does not invent a charging time.
