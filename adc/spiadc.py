#!/usr/bin/env python3

from .backends.backend import Backend

_WR = 0
_RD = 1


class SPIADC(object):
    """Generic SPI ADC"""

    def __init__(self, backend: Backend):
        self.backend = backend

    def read_reg(self, addr: int, length: int = 1) -> bytes:
        data = self.backend.transfer(bytes([addr << 1 | _RD]) + bytes(length))
        return data[1:]

    def write_reg(self, addr: int, value: bytes) -> None:
        self.backend.transfer(bytes([addr << 1 | _WR]) + value)
