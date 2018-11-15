#!/usr/bin/env python3

import pigpio

from .backend import Backend


class SPI_pigpio(Backend):

    def __init__(self, pi: pigpio.pi, spi_handle: int):
        self.pi = pi
        self.spi = spi_handle

    def transfer(self, data: bytes) -> bytes:
        _, data = self.pi.spi_xfer(self.spi, data)
        return bytes(data)

    def close(self):
        self.pi.spi_close(self.spi)
