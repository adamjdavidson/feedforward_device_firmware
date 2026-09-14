# Install Magic 8 firmware

You need a Mac, a USB-C **data** cable, and one Magic 8 device (Waveshare ESP32-C6-Touch-AMOLED-2.16). The package includes tools for Apple Silicon and Intel Macs. You do not need to type commands, install Python, or download anything else.

**Walkthrough candidate:** this package is for trying the download and installation process on a new device. Production battery-test instructions are not yet final.

## 1. Open the downloaded package

Unzip the downloaded Mac ZIP. Keep everything inside the **Magic 8 Firmware** folder together. You can move that whole folder, but do not move the installer or firmware out of it.

Use the complete ZIP attached to the release. GitHub's **Source code** ZIP and **Code → Download ZIP** are for developers and do not include a ready-to-install firmware image.

## 2. Connect one device

If the battery is already fitted, leave the case closed. If you are fitting a loose battery, follow **Fit the battery** below before connecting USB. Firmware installation itself can run on USB power.

Connect **one device at a time** with a USB-C data cable. A cable that only carries power cannot install firmware. Leave the device connected until installation finishes.

## 3. Double-click the installer

Open the **installer** folder and double-click **Install Magic 8.command**. A Terminal window opens and runs automatically. You do not type anything.

If macOS blocks the first launch:

1. Dismiss the warning without moving the file to Trash.
2. Open **System Settings → Privacy & Security**.
3. Find the message about **Install Magic 8.command** and click **Open Anyway**.
4. Confirm with your password or Touch ID if asked, then click **Open**. Double-click the installer again if it has not started.

This is a one-time approval for this downloaded copy. [Apple's instructions](https://support.apple.com/en-us/102445) describe the same approval path. The exact dialogs in this walkthrough still need checking on the recipient's Mac.

## 4. Wait for PASS

The installer checks its package, then shows progress while it writes and verifies the firmware. Leave the cable connected.

A successful installation ends with:

**PASS -- firmware installed and verified.**

Earlier prototype installations took under a minute. If it ends with **FAILED**, use the troubleshooting steps below. PASS confirms that the firmware was written and verified; check the screen next.

## 5. Check the device

Keep the USB cable connected for this walkthrough.

1. Let the device start. It should reach its dark navy resting screen.
2. Press the **third button, counting from the top of the case**. The cream **SHAKE ME** screen should appear.
3. Shake it deliberately. A move should appear after the swirl.
4. Tap anywhere on the screen for the extra sentence.
5. Tap again for the QR code and scan it with your phone. Confirm the page corresponds to the displayed move.

The third button wakes the device; pressing it while the device is awake does nothing. A tap after the QR screen returns it to rest. It also returns to rest after inactivity.

The small dot on the resting and SHAKE ME screens means:

- **Amber:** charging.
- **Green:** ready to use; charging can continue.
- **Solid red when unplugged:** low battery.
- **Blinking red:** needs attention. A unit with no battery fitted can show this; it is not by itself an installation failure.

A sleeping device may take a few seconds after USB is connected to show the charging dot.

## If installation fails

- **Package/checksum error:** download and unzip a fresh complete package. Do not mix files from different downloads.
- **More than one device found:** disconnect other USB serial devices, leaving only the Magic 8 connected, then run the installer again.
- **Device not found or connection timeout:** make sure only one device is connected; try a known data cable and a different USB port. For a device already running Magic 8, press the third button once after connecting USB.
- **Write or verification error:** unplug and reconnect, then retry once.
- **PASS but the device never starts:** retry once. If it still fails, set it aside and record the screen behavior.

If the same problem happens twice, stop on that unit. Keep a photo of the exact message and note which step failed.

## Battery testing after installation

The USB walkthrough above checks the software. It does not prove the battery is connected or taking charge.

A green dot is the firmware's readiness indication. Charging duration, a minimum charge before battery testing, and the middle-button power-off/start-up procedure have not yet been established for the production instructions. Record those observations during the walkthrough rather than treating an immediate failure to start on a newly fitted battery as a failed unit.

## Fit the battery

**Provisional assembly guide:** use this walkthrough to confirm that the supplied parts and case match these steps before preparing the batch.

Skip this section if the battery is already fitted. Keep USB disconnected while the case is open.

- The loose 3.7 V, 1000 mAh battery supplied with that unit — red and black
  wires ending in a small white two-pin plug.
- A **PH00 (`#00`) Phillips screwdriver**, preferably magnetized. The tip
  must fit the four rear screws cleanly without slipping.
- A **black polycarbonate insulating sheet** for each unit. The original
  packaging is supposed to include one; **for these units it is missing and
  has been bought separately**, as plain film. It must be black
  flame-retardant polycarbonate insulating film, 0.20–0.25 mm thick
  (8–10 mil), rated UL 94 V-0 or VTM-0, non-conductive, with no metal or
  foil in it.
- A clean microfiber cloth. The unit rests screen-down on this while open.
- A small cup or tray for the four screws.
- Optional: a few small pieces of 0.5 mm closed-cell EVA foam tape, used
  only if a battery rattles. Foam is **not** a substitute for the
  insulating sheet.

## Before you start

1. **Inspect the battery.** Do not use it if it is swollen, punctured,
   leaking, sharply creased or damaged in any way. Set it aside and use
   another.
2. **Do not remove or cut the orange tape** around the battery.
3. Make sure the USB-C cable is unplugged from the unit.
4. Clear a clean, dry work surface. Keep loose screws and metal objects
   away from the open circuit board.

## 1. Open the case

1. Put the folded microfiber cloth on the work surface.
2. Lay the unit screen-down on the cloth. Check there is no grit or hard
   object under the glass.
3. Remove the four rear screws and put them straight into the tray. They
   are small and there are no spares; a screw that rolls off the bench is
   gone.
4. Lift the rear cover straight up. If it sticks, work a fingernail or a
   plastic pick gently around the seam. **Never** put a metal tool into the
   seam, and never lever against the screen.

## 2. Find the right socket

With the cover off you are looking at the blue circuit board.

1. Find the metal USB-C socket at the edge of the board.
2. Right beside it is a much smaller two-pin socket, cream or white
   coloured.
3. The board is printed **`BAT`** next to that socket, with a **`+`** mark
   and a **`-`** mark.

In Waveshare's board photograph this socket is callout **7**:
[board photograph](https://docs.waveshare.com/assets/images/ESP32-C6-Touch-AMOLED-2.16-HW-444fe961eec158f8546e5a3df9e4863a.webp).

**Do not** plug the battery into the nearby speaker pads or into any other
connector. Only the one printed `BAT`.

## 3. Check polarity — this is the step that can destroy a unit

The plug is **not shaped to prevent going in backwards.** You have to
check it yourself, every time.

Turn the board so the word `BAT` reads the right way up:

```text
       +     BAT     -
      RED           BLACK
       [battery socket]
```

- The **red** wire must line up with the board's **`+`** mark.
- The **black** wire must line up with the board's **`-`** mark.

If the colours do not line up with those marks, **stop**. Do not insert the
plug, and do not try to force it round the other way. Set that unit and
that battery aside and report it.

(The board's schematic confirms pin 1 is battery positive and pin 2 is
ground: [schematic](https://files.waveshare.com/wiki/ESP32-C6-Touch-AMOLED-2.16/ESP32-C6-Touch-AMOLED-2.16-Schematic.pdf).)

## 4. Plug the battery in

1. Hold the white plastic plug itself. Never pull or push on the wires.
2. Hold it directly over the `BAT` socket.
3. Check one more time: red over `+`, black over `-`.
4. Push straight down, gently and evenly, on the plastic body.
5. If it tilts, resists, or needs real force — stop, take it out, check the
   orientation, try again.
6. Seated correctly, the plug sits level and fully in, with no gap and no
   metal contacts showing.

The unit **may** switch on by itself at this point, if that battery happens
to have some charge in it, or it may stay dark. **Either is fine** and
neither tells you anything yet.

## 5. Fit the insulating sheet and place the battery

The sheet is a required electrical barrier between the battery and the
board, not packaging.

1. **Cut one sheet carefully, then use it as the template for all the
   rest.** The film comes as a plain rectangle with no cutouts, and 150
   separately eyeballed cuts will not come out the same. Cut the first one,
   check it against the four points below, and once it passes, draw round
   it to make every other one. If a sheet does not pass, cut a new template
   — do not carry on with a bad one.
2. A sheet is good when all four are true:
   - it covers the whole area of the circuit board that the battery lies
     over, with no bare board showing at the edges of the battery;
   - it clears all four screw posts, so the cover still closes flat;
   - no part of it sits under a button or over a port;
   - there is a gap or notch for the battery wires to run back to the
     socket without being pinched.
3. Lay the sheet over the exposed circuit board.
4. Route the battery wires through the gap in a relaxed curve — not
   stretched, not sharply folded, not crossing a screw hole.
5. Lay the battery flat on top of the sheet, with its orange-taped wire end
   toward the `BAT` socket.
6. Never let the silver battery pouch touch the exposed circuit board.
7. Never bend, fold, squeeze, puncture or tightly tape the battery.

## 6. Check for rattle, add foam only if needed

1. Hold the rear cover in place with your fingers, without screws.
2. Tilt the unit once. Listen and feel for the battery shifting.
3. **Nothing moves?** Go straight to step 7. No foam.
4. **It rattles?** Take the cover off and stick one piece of 0.5 mm EVA
   foam, about 10 × 10 mm, to the inside centre of the **rear cover**,
   where it will just touch the flat face of the battery. Stick it to the
   cover, never to the battery, and keep it clear of the wires and screw
   posts.
5. Check again. The cover must sit flat without being pressed.
6. Use only as much foam as it takes to stop the movement.

The finished stack, from the back of the unit inward:

```text
rear cover
optional thin foam
battery
black insulating sheet
circuit board
screen
```

## 7. Close the case

1. Lower the cover on without shifting the battery.
2. Check all four sides. It must sit flat and flush **without** being
   pressed down.
3. If it rocks, bows, or leaves a gap, take it off and reposition the
   battery or the wires. Never use the screws to pull a bulging cover shut.
4. Start all four screws loosely.
5. Tighten diagonally: top-left, bottom-right, top-right, bottom-left.
6. Snug, not tight. You are screwing into plastic, and an overtightened
   screw strips the post or squeezes the battery.

---

