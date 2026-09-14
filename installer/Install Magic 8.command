#!/bin/bash
# Double-click to install the firmware included in this package.
# The USB writing tool is bundled; no Python, build tools or downloads needed.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"

finish() {
  local status="$1"
  if [ -t 0 ]; then read -rp "Press Enter to close this window..." _ || true; fi
  exit "$status"
}
fail() {
  echo
  echo "FAILED -- $1"
  echo "See START HERE.html in the downloaded folder."
  finish 1
}
cd "$ROOT" || exit 1

echo "=========================================="
echo " Magic 8 firmware installer"
echo "=========================================="
echo

shopt -s nullglob
images=(dist/magic8-*-esp32c6-merged.bin)
[ "${#images[@]}" -eq 1 ] || fail "Expected exactly one firmware image. Download a fresh complete package."
BIN="${images[0]}"
case "$BIN" in *-DEV-*) fail "This is a development image. Download the installation package instead." ;; esac

case "$(uname -m)" in
  arm64|aarch64) arch=arm64 ;;
  x86_64) arch=amd64 ;;
  *) fail "This package requires an Apple Silicon or Intel Mac." ;;
esac
ESPTOOL="installer/vendor/esptool-macos-$arch/esptool"
[ -x "$ESPTOOL" ] || fail "The bundled installation tool is missing or cannot run. Download and unzip the complete package again."

[ -f SHA256SUMS ] || fail "The package checksum file is missing. Download the complete package again."
# Confirm both required files are covered, as well as checking all manifest entries.
for file in "$BIN" "$ESPTOOL"; do
  checksum="$(shasum -a 256 "$file")" || fail "Could not read a package file."
  grep -Fqx -- "$checksum" SHA256SUMS || fail "A package checksum does not match. Download the complete package again."
done
shasum -a 256 -c SHA256SUMS >/dev/null 2>&1 || fail "A package checksum does not match. Download the complete package again."

# This board exposes native USB serial. Require one target, then bind esptool
# to that exact port instead of allowing it to search other serial devices.
ports=()
while IFS= read -r port; do
  [ -n "$port" ] && ports+=("$port")
done < <(find /dev -maxdepth 1 -name 'cu.usbmodem*' -print)
[ "${#ports[@]}" -gt 0 ] || fail "No device found. Connect one device with a data cable and try again."
[ "${#ports[@]}" -eq 1 ] || fail "Connect only one device. Disconnect other USB serial devices and try again."
PORT="${ports[0]}"

# macOS may require a one-time Open Anyway approval before this script can start.
# Once running, remove downloaded-file quarantine from the selected vendor tool.
if command -v xattr >/dev/null 2>&1; then
  if xattr -p com.apple.quarantine "$ESPTOOL" >/dev/null 2>&1; then
    xattr -d com.apple.quarantine "$ESPTOOL" 2>/dev/null || fail "macOS could not allow the bundled tool. Follow the Privacy & Security instructions in START HERE.html."
  fi
fi

echo "Firmware: $(basename "$BIN")"
echo "Keep ONE device connected using a USB-C DATA cable."
echo "Leave it connected until installation finishes."
echo
"$ROOT/$ESPTOOL" --chip esp32c6 --baud 460800 --port "$PORT" write-flash 0x0 "$ROOT/$BIN"
status=$?
echo
if [ "$status" -eq 0 ]; then
  echo "PASS -- firmware installed and verified."
  echo "Leave the device connected. Press the third button: SHAKE ME should appear."
else
  echo "FAILED -- firmware installation did not finish."
  echo "See START HERE.html before retrying."
fi
finish "$status"
