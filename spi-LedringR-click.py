from pynq import GPIO
import time
import spidev

# This will minipulate a LED Ring R Click Board in Slot 1
# of the Ultra96 mikro click mezzanine board 

# Obtain the reset pin of slot 1 of the Ultra96 mikro mezzanine board
# PS pin EMIO2 is connected to slot 1 RST
# PS pin EMIO3 is connected to slot 2 RST

# Linux pin number to Xilinx pin numbers are weird and have a large
# base number than can change between different releases of Linux
# The pynq base fcn will help here!
#mio_linux_number = GPIO.get_gpio_base() + 37

# EMIOs start after MIO and there
# is fixed offset for ZYNQ (54) and ZYNQ US+ (78)
emio_linux_number = GPIO.get_gpio_base() + 78 + 2

rst_pin = GPIO(emio_linux_number, 'out')

# Reset is usually active LOW
rst_pin.write(1)
time.sleep(.1)
rst_pin.write(0)
time.sleep(.1)
rst_pin.write(1)

print("Make the Click Led ring R board work!")

spi = spidev.SpiDev()
spi.open(1, 0)

# This Click board is just (4) 74HCP595 8-bit shift
# registers daisy chained to the SPI data bus.

n = 25  # How many steps around the loop
m = 100 # How many times 0xaa or 0x55

# All on
spi.xfer([0xff, 0xff, 0xff, 0xff])
time.sleep(.5)

data_to_send = 4 * [0x0]
for i in range(0,m):
    if i % 32 == 0:
        r = 0x1
    else:
        r = r << 1

    data_to_send[0] = r % 256
    data_to_send[1] = (r >> 8) % 256
    data_to_send[2] = (r >> 16) % 256
    data_to_send[3] = (r >> 24) % 256

    time.sleep(.01)

    spi.xfer(data_to_send)

for i in range(0,n):

    if i % 2 == 0:
        data_to_send = [0xaa, 0xaa, 0xaa, 0xaa]
    else:
        data_to_send = [0x55, 0x55, 0x55, 0x55]

    # You can send less than 1 byte at a time and a max of 4 bytes
    spi.xfer(data_to_send)

    # Slow it down so your eyes can see the blinking
    time.sleep(.07)

# Lights off
spi.xfer([0x00, 0x00, 0x00, 0x00])

print("End Test")

