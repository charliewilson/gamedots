# Keymap v1.0 - Charlie Wilson
# Example keymap for the Keybow 2040 macropad.

# Designed for CS2, but is a generic enough keymap that it can be
# bound for in many other games.

# 1. Connect Keybow to computer
# 2. Drop code.py and the lib folder into the root of the CIRCUITPY drive

# Imports
from pmk                     import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware
import usb_hid
from adafruit_hid.keyboard           import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode            import Keycode

# Set up Keybow
keybow = PMK(Hardware())
keys   = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout   = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap = [Keycode.FIVE,
          Keycode.Z,
          Keycode.A,
          None,
          Keycode.SHIFT,
          Keycode.X,
          Keycode.S,
          Keycode.W,
          Keycode.CONTROL,
          Keycode.C,
          Keycode.D,
          Keycode.E,
          Keycode.SPACE,
          Keycode.V,
          Keycode.G,
          Keycode.R]

# A secondary map of keycodes for the shifted layer
keymapShift = [Keycode.ESCAPE,
               Keycode.ONE,
               None,
               None,
               None,
               Keycode.TWO,
               None,
               None,
               Keycode.J,
               Keycode.THREE,
               None,
               Keycode.TAB,
               Keycode.T,
               Keycode.FOUR,
               Keycode.B,
               Keycode.F]

# The index of the map above that activates the second layer when held (top-left key)
layoutShiftKey = 3

# The variable that keeps track of if the layer is currently shifted
shifted = False

# The colour to set the keys when pressed, yellow.
# TODO: change this to something a bit nicer... or maybe even just white.
# I'm using non-shinethrough caps on this keyboard currently so it doesn't matter too much.
rgb = (255, 255, 0)

# Attach handler functions to all of the keys
for key in keys:

    # A press handler that sends the keycode and turns on the LED
    @keybow.on_press(key)
    def press_handler(key):
        global shifted

        if key.number == layoutShiftKey:
            shifted = True

        if shifted == True:
            keycode = keymapShift[key.number]
        else:
            keycode = keymap[key.number]

        if keycode:
            keyboard.press(keycode)

        key.set_led(*rgb)

    # A release handler that turns off the LED
    @keybow.on_release(key)
    def release_handler(key):
        global shifted

        if key.number == layoutShiftKey:
            shifted = False

        if keymap[key.number]:
            keyboard.release(keymap[key.number])
        if keymapShift[key.number]:
            keyboard.release(keymapShift[key.number])

        key.led_off()

# Always remember to call keybow.update()!
while True:
    keybow.update()
