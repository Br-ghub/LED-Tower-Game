from adafruit_circuitplayground import cp
import time
import board
import neopixel
import digitalio
delayGotten = False

button = digitalio.DigitalInOut(board.A3)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
button2 = digitalio.DigitalInOut(board.A4)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP
button_pressed = False
current_light = 0
cur = 0

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

def getDelay():
    global delayGotten, cur
    while True:
        pixels.fill((0, 0, 0, 0))
        pixels[cur] = (0, 0, 255, 0) #BRIAN: This was your bug((0, 0, 255, 0))
        #for i in range(cur): # BRIAN: Your bug was you were trying to loop through pixels, not a range:
        #    pixels[i] = (0, 0, 0, 0)#BRIAN: this was your bug((0, 0, 0, 0))
        if (not button2.value):
            cur = cur + 1
            if cur > 15:
                cur = 1
            time.sleep(.3)
            #BRIAN:  add a debounce!
        if (not button.value):
            if cur == 0: #BRIAN: don't return an int. Return a delay based on the int (or handle it somewhere) - or call it level
                return 0.08
            elif cur == 1:
                return 0.075
            elif cur == 2:
                return 0.07
            elif cur == 3:
                return 0.065
            elif cur == 4:
                return 0.06
            elif cur == 5:
                return 0.055
            elif cur == 6:
                return 0.05
            elif cur == 7:
                return 0.045
            elif cur == 8:
                return 0.04
            elif cur == 9:
                return 0.035
            elif cur == 10:
                return 0.03
            elif cur == 11:
                return 0.025
            elif cur == 12:
                return 0.02
            elif cur == 13:
                return 0.015
            elif cur == 14:
                return 0.01
            elif cur == 15:
                return 0.0001
            delayGotten = True

def zoom(colour, delay):
    global button_pressed, current_light
    for i in range(NUM_PIXELS):
        pixels.fill((0, 0, 0, 0))
        pixels[i] = colour
        time.sleep(delay)
        if (not button.value):
            button_pressed = True
            current_light = i
            break

def zoom_but_BACKWARDS_QUESTIONMARK(colour, delay):
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

def play(delay):
    global button_pressed, current_light, delayGotten
    time.sleep(1)
    button_pressed = False
    current_light = 0
    while button_pressed == False:
        zoom((132, 132, 230, 0), delay)
        if button_pressed == True:
            break
        zoom_but_BACKWARDS_QUESTIONMARK((132, 132, 230, 0), delay)
    if current_light != 15:
        loser(current_light, (139, 0, 0, 0))
    if current_light == 15:
        winner()
        time.sleep(5)
        pixels.fill((0, 0, 0, 0))
    delayGotten = False

while True:
    pixels.fill((0, 0, 0, 0))
    if delayGotten == False:
        delay = getDelay()
    if (not button.value):
        play(delay)