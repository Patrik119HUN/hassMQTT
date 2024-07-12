from loguru import logger
from .abstract_driver import AbstractDriver
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from smbus import SMBus


IODIRA = 0x00  # Pin direction register
IODIRB = 0x01  # Pin direction register
IPOLA = 0x02
IPOLB = 0x03
GPINTENA = 0x04
GPINTENB = 0x05
DEFVALA = 0x06
DEFVALB = 0x07
INTCONA = 0x08
INTCONB = 0x09
IOCONA = 0x0A
IOCONB = 0x0B
GPPUA = 0x0C
GPPUB = 0x0D

INTFA = 0x0E
INTFB = 0x0F
INTCAPA = 0x10
INTCAPB = 0x11
GPIOA = 0x12
GPIOB = 0x13
OLATA = 0x14
OLATB = 0x15
ALL_OFFSET = [
    IODIRA,
    IODIRB,
    IPOLA,
    IPOLB,
    GPINTENA,
    GPINTENB,
    DEFVALA,
    DEFVALB,
    INTCONA,
    INTCONB,
    IOCONA,
    IOCONB,
    GPPUA,
    GPPUB,
    GPIOA,
    GPIOB,
    OLATA,
    OLATB,
]

BANK_BIT = 7
MIRROR_BIT = 6
SEQOP_BIT = 5
DISSLW_BIT = 4
HAEN_BIT = 3
ODR_BIT = 2
INTPOL_BIT = 1

GPA0 = 0
GPA1 = 1
GPA2 = 2
GPA3 = 3
GPA4 = 4
GPA5 = 5
GPA6 = 6
GPA7 = 7
GPB0 = 8
GPB1 = 9
GPB2 = 10
GPB3 = 11
GPB4 = 12
GPB5 = 13
GPB6 = 14
GPB7 = 15
ALL_GPIO = [
    GPA0,
    GPA1,
    GPA2,
    GPA3,
    GPA4,
    GPA5,
    GPA6,
    GPA7,
    GPB0,
    GPB1,
    GPB2,
    GPB3,
    GPB4,
    GPB5,
    GPB6,
    GPB7,
]

INPUT = 0xFF
OUTPUT = 0x00


class MCP23017:
    def __init__(self, address: int, i2c: SMBus):
        self.i2c = i2c
        self.address = address

    def set_all_output(self):
        self.i2c.write_byte_data(self.address, IODIRA, 0x00)
        self.i2c.write_byte_data(self.address, IODIRB, 0x00)

    def set_all_input(self):
        self.i2c.write_byte_data(self.address, IODIRA, 0xFF)
        self.i2c.write_byte_data(self.address, IODIRB, 0xFF)

    def pin_mode(self, gpio, mode):
        pair = self.get_offset_gpio_tuple([IODIRA, IODIRB], gpio)
        self.set_bit_enabled(pair[0], pair[1], True if mode is INPUT else False)

    def digital_write(self, gpio, direction: bool):
        pair = self.get_offset_gpio_tuple([OLATA, OLATB], gpio)
        self.set_bit_enabled(pair[0], pair[1], direction)

    def digital_read(self, gpio):
        pair = self.get_offset_gpio_tuple([GPIOA, GPIOB], gpio)
        bits = self.i2c.read_byte_data(self.address, pair[0])
        return True if (bits & (1 << pair[1])) > 0 else False

    def digital_read_all(self):
        return [
            self.i2c.read_byte_data(self.address, GPIOA),
            self.i2c.read_byte_data(self.address, GPIOB),
        ]

    def get_offset_gpio_tuple(self, offsets, gpio):
        if offsets[0] not in ALL_OFFSET or offsets[1] not in ALL_OFFSET:
            raise TypeError(
                "offsets must contain a valid offset address. See description for help"
            )
        if gpio not in ALL_GPIO:
            raise TypeError("pin must be one of GPAn or GPBn. See description for help")

        offset = offsets[0] if gpio < 8 else offsets[1]
        _gpio = gpio % 8
        return (offset, _gpio)

    def set_bit_enabled(self, offset, gpio, enable):
        stateBefore = self.i2c.read_byte_data(self.address, offset)
        value = (
            (stateBefore | self.bitmask(gpio))
            if enable
            else (stateBefore & ~self.bitmask(gpio))
        )
        self.i2c.write_byte_data(self.address, offset, value)

    def bitmask(self, gpio):
        return 1 << (gpio % 8)


class GPIODriver(AbstractDriver):
    def __init__(self):
        __i2c_bus = SMBus(1)
        __address = 0x20
        self.__gpio = MCP23017(__address, __i2c_bus)

    def connect(self, *args, **kwargs):
        self.__gpio.pin_mode(kwargs["address"], kwargs["mode"])

    def disconnect(self):
        pass

    def send_data(self, address: int, value: bool):
        self.__gpio.digital_write(address, value)

    def get_data(self, address: int):
        return self.__gpio.digital_read(address)
