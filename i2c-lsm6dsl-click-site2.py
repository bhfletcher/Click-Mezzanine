from pynq import GPIO
import time
import smbus  # Must sudo apt install python3-smbus !

# This will minipulate a ST LPS22HB Click in Slot 1
# of the Ultra96 mikro click mezzanine board 

## Obtain the reset pin of slot 1 of the Ultra96 mikro mezzanine board
# PS pin EMIO2 is connected to slot 1 RST
# PS pin EMIO3 is connected to slot 2 RST

# Linux pin number to Xilinx pin numbers are weird and have a large
# base number than can change between different releases of Linux
# The pynq base fcn will help here!
#mio_linux_number = GPIO.get_gpio_base() + 37

# EMIOs start after MIO and there
# is fixed offset for ZYNQ (54) and ZYNQ US+ (78)
# offset = 2 corresonds to mikroBUS site 1 on Click Mezzanine v1.03
#   HD_GPIO_7
# offset = 9? corresonds to mikroBUS site 2 on Click Mezzanine v1.03
#   HD_GPIO_14

emio_linux_number = GPIO.get_gpio_base() + 78 + 2

rst_pin = GPIO(emio_linux_number, 'out')

# Convert signed into unsigned from i2c read byte
def i2c_read_byte(i2c, DA, DR):
    return (0xff & i2c.read_byte_data(DA, DR))

def i2c_write_byte(i2c, DA, DR, val):
    return (i2c.write_byte_data(DA, DR, val))

# Reset is usually active LOW, hold Click in reset while I2C is setup
# and reset the i2c mux
#rst_pin.write(0)
#time.sleep(.1)
# Unreset the click board
#rst_pin.write(1)
#time.sleep(.3)

print("Start I2C Test\n")

# There is an I2C mux chip on the Ultra96.  Linux has the mux driver
# enabled so the click slot 1 is /dev/i2c-2 and slot 2 is /dev/i2c-3
i2c_bus = smbus.SMBus(3)  # 2 = /dev/i2c-2, 3 = /dev/i2c-3 etc.

# The ST LPS22HB registers can be found in the data sheet:
#DA = 0x5c  # Device Address for Touchpad chip is setup for 0x25
DA = 0x6a  # Device Address for LSM6DSL chip is setup for 0x6a when SDO=GND

WHO_AM_I_REG = 0xf
# Expected value for LSM6DSL is 01101010b = 0x6A
expected_val = 0x6A
data = i2c_read_byte(i2c_bus, DA, WHO_AM_I_REG)
print(hex(data))
print("Expected value =")
print(hex(expected_val))

CTRL1_XL_REG = 0x10
expected_val = 0x00
data = i2c_read_byte(i2c_bus, DA, CTRL1_XL_REG)
print(hex(data))
print("Expected value =")
print(hex(expected_val))

print("Writing new data")
write_val = 0x66
i2c_write_byte(i2c_bus, DA, CTRL1_XL_REG, write_val)
time.sleep(.3)

expected_val = write_val
data = i2c_read_byte(i2c_bus, DA, CTRL1_XL_REG)
print(hex(data))
print("Expected value =")
print(hex(expected_val))
print("\n")


print("End I2C Test")
