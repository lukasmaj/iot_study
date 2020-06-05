from pynput.keyboard import Key, Controller, Listener
import time
import gpio

FAKE_ON_OF = 21
FAKE_SENSOR = 16

gpio.use_pin([FAKE_ON_OF, FAKE_SENSOR])
time.sleep(2)
gpio.set_as_output(FAKE_ON_OF)
gpio.set_as_output(FAKE_SENSOR)

def on_press(key):
    if key == Key.up:
        gpio.set_pin(FAKE_ON_OF)
    if key == Key.down:
        gpio.set_pin(FAKE_SENSOR)

def on_release(key):
    if key == Key.up:
        gpio.clear_pin(FAKE_ON_OF)
    if key == Key.down:
        gpio.clear_pin(FAKE_SENSOR)
    if key == Key.esc:
        print "Exit"
        gpio.unuse_pin([FAKE_ON_OF, FAKE_SENSOR])
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()