import spidev

print("Start SPI Test\n")

spi = spidev.SpiDev()
spi.open(0, 0)
data_to_send = [0x01, 0x02, 0x03]
data_read_back = spi.xfer(data_to_send)

print("Read back:")
for i in data_read_back:
    print(hex(i))

print("\nEnd SPI Test")

