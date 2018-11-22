#!/usr/bin/env python3

try:
    from .ext import spi_rpi
except ImportError:
    pass

import pigpio

from .backend import Backend


class SPI_pigpio(Backend):

    def __init__(self, pi: pigpio.pi, ch: int, baud: int, data_ready_pin: int):
        self.pi = pi
        self.ch = ch
        self.baud = baud
        self.dr_pin = data_ready_pin

        pi.set_mode(data_ready_pin, pigpio.INPUT)
        pi.set_pull_up_down(data_ready_pin, pigpio.PUD_UP)

    def transfer(self, data: bytes) -> bytes:
        spi = self.pi.spi_open(self.ch, self.baud)
        _, data = self.pi.spi_xfer(spi, data)
        self.pi.spi_close(spi)
        return bytes(data)

    def get_data(self, addr: int, byte_width: int, sample_len: int) -> [int]:
        assert 2 <= byte_width <= 3
        return spi_rpi.get_data(self.ch, self.baud, self.dr_pin, addr, byte_width, sample_len)

    def close(self):
        pass
