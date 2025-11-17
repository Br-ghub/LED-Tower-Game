from adafruit_circuitplayground import cp
import time
import board
import neopixel
import digitalio

button = digitalio.DigitalInOut(board.A3)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
button_pressed = False
current_light = 0

# Setup for RGBW strip
PIXEL_PIN = board.A1
NUM_PIXELS = 16

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=0.1,
    auto_write=True,
    bpp=4,
    pixel_order=neopixel.GRBW
)

def zoom(colour, delay = 0.01):
    global button_pressed, current_light
    for i in range(NUM_PIXELS):
        pixels.fill((0, 0, 0, 0))
        pixels[i] = colour
        time.sleep(delay)
        if (not button.value):
            button_pressed = True
            current_light = i
            break

def zoom_but_BACKWARDS_QUESTIONMARK(colour, delay = 0.01):
    global button_pressed, current_light
    for i in reversed(range(NUM_PIXELS)):
        pixels.fill((0, 0, 0, 0))
        pixels[i] = colour
        time.sleep(delay)
        if (not button.value):
            button_pressed = True
            current_light = i
            break

def winner(delay = 0.05):
    global current_light
    i = 0
    while i < 6:
        pixels.fill((34, 139, 34, 0))
        time.sleep(delay)
        if i < 5:
            pixels.fill((0, 0, 0, 0))
            time.sleep(delay)
        i = i + 1
    cp.play_file("correct.wav")
    current_light = 0

def loser(current_light, colour, delay = 0.15):
    for light in reversed(range(current_light, -1, -1)):
        pixels[light] = colour
    cp.play_file("wrong.wav")
    for light in range(current_light, -1, -1):
        pixels[light] = ((0, 0, 0, 0))
        time.sleep(delay)

def play():
    global button_pressed, current_light
    time.sleep(1)
    button_pressed = False
    current_light = 0
    while button_pressed == False:
        zoom((132, 132, 230, 0))
        if button_pressed == True:
            break
        zoom_but_BACKWARDS_QUESTIONMARK((132, 132, 230, 0))
    if current_light != 15:
        loser(current_light, (139, 0, 0, 0))
    if current_light == 15:
        winner()
        time.sleep(5)
        pixels.fill((0, 0, 0, 0))

while True:
    pixels.fill((0, 0, 0, 0))
    if (not button.value):
        play()