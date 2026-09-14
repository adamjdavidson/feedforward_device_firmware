# Prepare a Mac firmware download

This is the maintainer procedure. Device operators use [the installation guide](INSTALLATION.md).

## Build the firmware in its source repository

Use a clean checkout of an approved, reviewed commit in `adamjdavidson/magic8-device-firmware`. Update `VERSION` through its normal PR workflow for each new release. Activate its documented ESP-IDF toolchain and run:

```sh
python3 flashing/build_release.py
```

Do not use `--dev`. The firmware builder enforces console shake disabled, light sleep enabled, the full approved content and exact URLs, and a clean tree. Preserve its successful build log. The public package builder consumes that merged image; it does not replace or bypass those firmware checks.

Record the source checkout's full commit SHA. The image must be freshly produced from that checkout, not an older file selected from elsewhere.

## Build the download here

Clone this repository. For package preparation only, install Python 3 and the pinned build dependency into a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-build.txt
python -m unittest discover -s tests -v
python tools/package.py --firmware /absolute/path/to/magic8-VERSION-esp32c6-merged.bin --source-commit FULL_FIRMWARE_COMMIT_SHA
```

Substitute the real image path and its source SHA. Run this from a clean, committed installer checkout so `release.json` records the code that actually produced the ZIP. The command writes `packages/Magic8-Firmware-VERSION-mac.zip` and its `.zip.sha256` file.

`README.md` is the single source for `START HERE.html`; `docs/BATTERY.md` produces `FIT BATTERY.html`. The package includes the six named photos under `docs/images/`, and rewrites links so both guides and their photos work offline. `docs/guide.css` controls their typography. The builder uses an explicit allowlist, bundles only the two esptool executables and licenses, includes exactly one firmware image, and records both firmware and installer source commits. The ZIP retains executable permissions. `SHA256SUMS` covers every included file except itself. The installer checks those sums before writing to USB. Checksums detect corruption; they are not a signature authenticating the publisher.

CI also runs each real bundled esptool executable on its matching Apple Silicon or Intel Mac runner, using the version command without accessing USB.

The package builder rejects development filenames, empty images and uncommitted installer files. It cannot establish whether someone renamed an arbitrary binary or supplied a false source SHA: the guarded source build and maintainer's verified provenance remain required.

## Verify and publish

1. Inspect and extract the ZIP outside both source checkouts. Verify its archive checksum, then the extracted `SHA256SUMS`.
2. Confirm that the included image hash matches the guarded source build. Check `release.json` identifies the source commits used.
3. Test the actual browser download and double-click launch, including any macOS approval dialog. Do not substitute a terminal launch or manually added quarantine for this observation.
4. Install that exact package on the intended board and capture its first boot version. Walk wake, shake, more text and QR scan with a person watching the screen.
5. Record each result and remaining unknown in release notes. A package still awaiting these observations must remain a GitHub **pre-release**, labeled as a walkthrough candidate. Publish no claim that the production batch is ready until its physical checks and assembly/charging instructions are complete.

Use a release asset named `Magic8-Firmware-VERSION-mac.zip`, plus its `.zip.sha256`. Update the README download and release-notes links when a new package replaces it. For instructions-only revisions, keep the firmware image and version unchanged and publish under a new descriptive tag (for example `v0.2.1-guide2`); never silently replace an earlier published ZIP. GitHub-generated source archives are not installation packages.

## Update the bundled tool

The bundled tool's version and source links live in `THIRD_PARTY.md`. Any tool update must include both Mac architectures, preserve the upstream license files, update the version in `tools/package.py`, and rerun package and device checks.
