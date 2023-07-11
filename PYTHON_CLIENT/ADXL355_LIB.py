import wiringpi as wp
from time import time, sleep
from spidev import SpiDev

# SPI config
SPI_MAX_CLOCK_HZ = 4000000
SPI_MODE = 0b00
SPI_BUS = 0
SPI_DEVICE = 0

# DRDY config
DRDY_PIN = 11              # Raspberry Pi GPIO pin for DRDY cable
DRDY_DELAY = 0.000001      # Delay while polling DRDY pin in seconds
DRDY_TIMEOUT = 1           # Delay to check DRDY pin in seconds


# Register addresses
REG_DEVID_AD = 0x00
REG_DEVID_MST = 0x01
REG_PARTID = 0x02
REG_REVID = 0x03
REG_STATUS = 0x04
REG_FIFO_ENTRIES = 0x05
REG_TEMP2 = 0x06
REG_TEMP1 = 0x07
REG_XDATA3 = 0x08
REG_XDATA2 = 0x09
REG_XDATA1 = 0x0A
REG_YDATA3 = 0x0B
REG_YDATA2 = 0x0C
REG_YDATA1 = 0x0D
REG_ZDATA3 = 0x0E
REG_ZDATA2 = 0x0F
REG_ZDATA1 = 0x10
REG_FIFO_DATA = 0x11
REG_OFFSET_X_H = 0x1E
REG_OFFSET_X_L = 0x1F
REG_OFFSET_Y_H = 0x20
REG_OFFSET_Y_L = 0x21
REG_OFFSET_Z_H = 0x22
REG_OFFSET_Z_L = 0x23
REG_ACT_EN = 0x24
REG_ACT_THRESH_H = 0x25
REG_ACT_THRESH_L = 0x26
REG_ACT_COUNT = 0x27
REG_FILTER = 0x28
REG_FIFO_SAMPLES = 0x29
REG_INT_MAP = 0x2A
REG_SYNC = 0x2B
REG_RANGE = 0x2C
REG_POWER_CTL = 0x2D
REG_SELF_TEST = 0x2E
REG_RESET = 0x2F


# Measaurement range definition
RANGE_2G = 0b01
RANGE_4G = 0b10
RANGE_8G = 0b11


# ODR and low-pass filter corner definition
# Data rate-lowpass corner
ODR_4000 = 0b0000       # 4000-1000 Hz
ODR_2000 = 0b0001       # 2000-500 Hz
ODR_1000 = 0b0010       # 1000-250 Hz
ODR_500 = 0b0011       # 500-125 Hz
ODR_250 = 0b0100       # 250-62.5 Hz
ODR_125 = 0b0101       # 125-31.5 Hz
ODR_62_5 = 0b0110       # 62.5-15.625 Hz
ODR_31_25 = 0b0111       # 31.25-7.813 Hz
ODR_15_625 = 0b1000       # 15.625-3.906 Hz
ODR_7_813 = 0b1001       # 7.813-1.95 3Hz
ODR_3_906 = 0b1010       # 3.906-0.977 Hz


# High-pass filter corner definition
HPFC_0 = 0b000          # No high-pass filter
HPFC_1 = 0b001          # 24.70 x 10-4 x ODR
HPFC_2 = 0b010          # 6.208 x 10-4 x ODR
HPFC_3 = 0b011          # 1.554 x 10-4 x ODR
HPFC_4 = 0b100          # 0.386 x 10-4 x ODR
HPFC_5 = 0b101          # 0.095 x 10-4 x ODR
HPFC_6 = 0b110          # 0.023 x 10-4 x ODR


RANGE_TO_BIT = {2.048: RANGE_2G,
                4.096: RANGE_4G,
                8.192: RANGE_8G}


ODR_TO_BIT = {4000: ODR_4000,
              2000: ODR_2000,
              1000: ODR_1000,
              500: ODR_500,
              250: ODR_250,
              125: ODR_125,
              62.5: ODR_62_5,
              31.25: ODR_31_25,
              15.625: ODR_15_625,
              7.813: ODR_7_813,
              3.906: ODR_3_906}


HPFC_TO_BIT = {0: HPFC_0,
               1: HPFC_1,
               2: HPFC_2,
               3: HPFC_3,
               4: HPFC_4,
               5: HPFC_5,
               6: HPFC_6}


class ADXL355():
    def __init__(self):
        # SPI init
        self.spi = SpiDev()
        self.spi.open(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_MAX_CLOCK_HZ
        self.spi.mode = SPI_MODE

        wp.wiringPiSetupPhys()                  # Use physical pin numbers
        self.drdy_pin = DRDY_PIN                # Define Data Ready pin
        self.drdy_delay = DRDY_DELAY            # Define Data Ready delay
        self.drdy_timeout = DRDY_TIMEOUT        # Define Data Ready timeout

        # Default device parameters
        RANGE = 2.048
        ODR = 125
        HPFC = 0

        # Device init
        self.transfer = self.spi.xfer2
        self.setrange(RANGE)                    # Set default measurement range
        # Set default ODR and filter props
        self.setfilter(ODR, HPFC)
        self.waitdrdy()

        self.factor = (RANGE * 2) / 2 ** 20     # Instrument factor raw to g

    def read(self, register, length=1):
        address = (register << 1) | 0b1
        if length == 1:
            result = self.transfer([address, 0x00])
            return result[1]
        else:
            result = self.transfer([address] + [0x00] * (length))
            return result[1:]

    def write(self, register, value):
        # Shift register address 1 bit left, and set LSB to zero
        address = (register << 1) & 0b11111110
        result = self.transfer([address, value])

    def waitdrdy(self):
        start = time()
        elapsed = time() - start
        # Wait DRDY pin to go low or DRDY_TIMEOUT seconds to pass
        if self.drdy_pin is not None:
            drdy_level = wp.digitalRead(self.drdy_pin)
            while (drdy_level == wp.LOW) and (elapsed < self.drdy_timeout):
                elapsed = time() - start
                drdy_level = wp.digitalRead(self.drdy_pin)
                # Delay in order to avoid busy wait and reduce CPU load.
                sleep(self.drdy_delay)
            if elapsed >= self.drdy_timeout:
                print("\nTimeout while polling DRDY pin")
        else:
            sleep(self.drdy_timeout)
            print("\nDRDY Pin did not connected")

    def fifofull(self):
        return self.read(REG_STATUS) & 0b10

    def fifooverrange(self):
        return self.read(REG_STATUS) & 0b100

    def start(self):
        tmp = self.read(REG_POWER_CTL)
        self.write(REG_POWER_CTL, tmp & 0b0)

    def stop(self):
        tmp = self.read(REG_POWER_CTL)
        self.write(REG_POWER_CTL, tmp | 0b1)

    def twocomp(self, value):
        if (0x80000 & value):
            ret = - (0x0100000 - value)
            # from ADXL355_Acceleration_Data_Conversion function from EVAL-ADICUP360 repository
            # value = value | 0xFFF00000
        else:
            ret = value
        return ret

    def setrange(self, r):
        self.stop()
        temp = self.read(REG_RANGE)
        self.write(REG_RANGE, (temp & 0b11111100) | RANGE_TO_BIT[r])
        self.start()

    def setfilter(self, lpf, hpf):
        self.stop()
        self.write(REG_FILTER, (HPFC_TO_BIT[hpf] << 4) | ODR_TO_BIT[lpf])
        self.start()

    def getXRaw(self):
        datal = self.read(REG_XDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.twocomp(res)
        return res

    def getYRaw(self):
        datal = self.read(REG_YDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.twocomp(res)
        return res

    def getZRaw(self):
        datal = self.read(REG_ZDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.twocomp(res)
        return res

    def getX(self):
        return float(self.getXRaw()) * self.factor

    def getY(self):
        return float(self.getYRaw()) * self.factor

    def getZ(self):
        return float(self.getZRaw()) * self.factor

    def getTempRaw(self):
        high = self.read(REG_TEMP2)
        low = self.read(REG_TEMP1)
        res = ((high & 0b00001111) << 8) | low
        return res

    def getTemp(self, bias=1852.0, slope=-9.05):
        temp = self.temperatureRaw()
        res = ((temp - bias) / slope) + 25
        return res

    def get3Vfifo(self):
        res = []
        x = self.read(REG_FIFO_DATA, 3)
        while (x[2] & 0b10 == 0):
            y = self.read(REG_FIFO_DATA, 3)
            z = self.read(REG_FIFO_DATA, 3)
            res.append([x, y, z])
            x = self.read(REG_FIFO_DATA, 3)
        return res

    def emptyfifo(self):
        x = self.read(REG_FIFO_DATA, 3)
        while (x[2] & 0b10 == 0):
            x = self.read(REG_FIFO_DATA, 3)

    def hasnewdata(self):
        res = self.read(REG_STATUS)
        if res & 0b1:
            return True
        return False

    def fastgetsamples(self, sampleno=1000):
        """Get specified numbers of samples from FIFO, without any processing.

        This function is needed for fast sampling, without loosing samples. While FIFO should be enough for many situations, there is no check for FIFO overflow implemented (yet).
        """
        res = []
        while (len(res) < sampleno):
            res += self.get3Vfifo()
        return res[0:sampleno]

    def getsamplesRaw(self, sampleno=1000):
        """Get specified numbers of samples from FIFO, and process them into signed integers"""
        data = self.fastgetsamples(sampleno)
        return self.convertlisttoRaw(data)

    def getsamples(self, sampleno=1000):
        """Get specified numbers of samples from FIFO, process and convert to g values"""
        data = self.getsamplesRaw(sampleno)
        return self.convertRawtog(data)

    def convertlisttoRaw(self, data):
        """Convert a list of 'list' style samples into signed integers"""
        res = []
        for i in range(len(data)):
            row3v = []
            for j in range(3):
                low = (data[i][j][2] >> 4)
                mid = (data[i][j][1] << 4)
                high = (data[i][j][0] << 12)
                value = 1 * self.twocomp(low | mid | high)
                row3v.append(value)
            res.append(row3v)
        return res

    def convertRawtog(self, data):
        """Convert a list of raw style samples into g values"""
        res = [[d[0] * self.factor, d[1] * self.factor, d[2] * self.factor]
               for d in data]
        return res

    def getAxisRaw(self):
        self.waitdrdy()
        return self.getXRaw(), self.getYRaw(), self.getZRaw()

    def getAxis(self):
        self.waitdrdy()
        return self.getX(), self.getY(), self.getZ()
