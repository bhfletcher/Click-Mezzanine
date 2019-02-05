from pynq import GPIO
import time
import smbus

# This will minipulate a LED Ring R Click Board in Slot 1
# of the Ultra96 mikro click mezzanine board 

# Obtain the reset pin of slot 1 of the Ultra96 mikro mezzanine board
# PS pin MIO37 is connected to slot 1 RST
# PS pin MIO40 is connected to slot 2 RST

# Linux pin number to Xilinx pin numbers are weird and have a large
# base number than can change between different releases of Linux
# The pynq base fcn will help here!  base for 2018.2 was 338
mio_linux_number = GPIO.get_gpio_base() + 37

# EMIOs start after MIO and there
# is fixed offset for ZYNQ (54) and ZYNQ US+ (78)
#   emio_linux_number = GPIO.get_gpio_pin(emio_offset)

rst_pin = GPIO(mio_linux_number, 'out')

# Reset is usually active LOW
rst_pin.write(1)
time.sleep(.1)
rst_pin.write(0)
time.sleep(.1)
rst_pin.write(1)

print("Start I2C Test\n")

print("\nEnd I2C Test")

