import board
import displayio
import terminalio
import digitalio
import time
import busio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_tsl2561
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

displayio.release_displays()

ow_bus = OneWireBus(board.GP16)
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])


# Use for I2C
SDA = board.GP8
SCL = board.GP9
i2c = busio.I2C(SCL, SDA)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

sensor = adafruit_tsl2561.TSL2561(i2c)
# 0x57

# Enable the light sensor
sensor.enabled = True
time.sleep(1)
 
# Set gain 0=1x, 1=16x
sensor.gain = 0
 
# Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
sensor.integration_time = 1
 
print("Getting readings...")
 
# Get raw (luminosity) readings individually
broadband = sensor.broadband
infrared = sensor.infrared
 
# Get raw (luminosity) readings using tuple unpacking
# broadband, infrared = tsl.luminosity
 
# Get computed lux value (tsl.lux can return None or a float)


# Disble the light sensor (to save power)
sensor.enabled = True

display_bus = displayio.I2CDisplay(i2c, device_address=60)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

if(i2c.try_lock()):
    print("i2c.scan(): " + str(i2c.scan()))
    i2c.unlock()
print()

# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw a label
text = "Raspberry Pi Pico"
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=16, y=5
)
name = label.Label(
    terminalio.FONT, text="Sunat P.", color=0xFFFFFF, x=42, y=20
)
light = label.Label(
    terminalio.FONT, text=" ", color=0xFFFFFF, x=15, y=35
)
temp = label.Label(
    terminalio.FONT, text=" ", color=0xFFFFFF, x=26, y=50
    )
splash.append(text_area)
splash.append(name)
splash.append(light)
splash.append(temp)
while True:
    temp.text = str("Temp: %0.2f C" % ds18.temperature)
    if sensor.lux is not None: 
        if sensor.lux > 50.0:
            light.text = "Light: %0.3f Lux" % sensor.lux
            led.value = False
        elif sensor.lux < 50.0 and sensor.lux > 0.1:
            light.text = "Light: %0.3f Lux" % sensor.lux
            led.value = True

    else:
        light.text = "Cannot measure!!"
        led.value = True
        

