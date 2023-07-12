
from spidev import SpiDev

class MCP3008:
    """
    Class to interact with the MCP3008 ADC.
    """
    def __init__(self, bus=0, device=0):
        """
        Initialize MCP3008.

        Args:
        bus (int): SPI bus number.
        device (int): SPI device number.
        """
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

    def open(self):
        """
        Open the SPI connection.
        """
        self.spi.open(self.bus, self.device)

    def read(self, channel=0):
        """
        Read from the MCP3008.

        Args:
        channel (int): Channel number to read from.

        Returns:
        data (int): Read data.
        """
        cmd1 = 4 | 2 | ((channel & 4) >> 2)
        cmd2 = (channel & 3) << 6

        adc = self.spi.xfer2([cmd1, cmd2, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data

    def close(self):
        """
        Close the SPI connection.
        """
        self.spi.close()
