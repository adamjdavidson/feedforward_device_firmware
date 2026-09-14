# Magic 8 firmware

Install the Magic 8 AI device's firmware from a Mac. Download one ZIP, connect one device, and double-click **Install Magic 8.command**. No commands or software installation required.

**[Download for Mac — version 0.2.1](https://github.com/adamjdavidson/magic8-firmware/releases/download/v0.2.1-walkthrough/Magic8-Firmware-0.2.1-mac.zip)**

This first package is a **walkthrough candidate**. Its download, first launch and new-device checks are being tried before the production handoff. See the [release notes](https://github.com/adamjdavidson/magic8-firmware/releases/tag/v0.2.1-walkthrough) for what has been verified.

## Install

1. Download the ZIP above. Use that packaged download, rather than GitHub's **Code → Download ZIP** or **Source code** archives.
2. Unzip it and open **START HERE.html**.
3. Follow the guide to connect one device and double-click **installer/Install Magic 8.command**.
4. Wait for **PASS — firmware installed and verified**, then check the device.

[Read the full instructions](docs/INSTALLATION.md), including battery fitting and what to do if macOS asks for approval.

## Code in this repository

- `installer/Install Magic 8.command` — the double-click Mac installer.
- `installer/vendor/` — bundled tools for Apple Silicon and Intel Macs.
- `docs/INSTALLATION.md` — source for the included HTML guide.
- `tools/package.py` — builds the complete ZIP and checksum files.
- `tests/` — checks installation failure handling and package contents without writing to hardware.
- [Release procedure](docs/RELEASE.md) — how to prepare, verify and publish a package.

The device firmware is developed in the separate `adamjdavidson/magic8-device-firmware` repository. This repository contains the installation code and distributes the compiled device firmware. Every ZIP records the firmware source commit and image checksum in `release.json`.

See [bundled software notices](THIRD_PARTY.md).
