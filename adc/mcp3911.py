#!/usr/bin/env python3

from .mcp3911_register import *
from .spiadc import SPIADC


class MCP3911(SPIADC):
    """24bit 2ch ADC"""

    def read_data_array(self, length: int, ch=0, width=24) -> [int]:
        assert ch in [0, 1], 'ADC channel must be 0 or 1'
        assert width in [16, 24], 'width must be 16 or 24'

        addr = Address.CHANNEL0 if ch == 0 else Address.CHANNEL1
        byte_width = 2 if width == 16 else 3

        data = self.backend.get_data(addr, byte_width, length)

        if width == 16:
            for i in range(length):
                x = data[i]
                if x > 32768:
                    x -= 65536
                data[i] = x
        else:
            for i in range(length):
                x = data[i]
                if x > 8388608:
                    x -= 16777216
                data[i] = x

        return data

    def read_data(self, ch=0, width=24) -> int:
        return self.read_data_array(1, ch, width)[0]

    def read_reg_gain(self) -> GainReg:
        return GainReg.from_bytes(self.read_reg(Address.GAIN))

    def read_reg_status_com(self) -> StatusComReg:
        return StatusComReg.from_bytes(self.read_reg(Address.STATUSCOM, 2))

    def read_reg_config(self) -> ConfigReg:
        return ConfigReg.from_bytes(self.read_reg(Address.CONFIG, 2))

    def write_reg_gain(self, reg: GainReg) -> None:
        self.write_reg(Address.GAIN, bytes(reg))

    def write_reg_status_com(self, reg: StatusComReg) -> None:
        self.write_reg(Address.STATUSCOM, bytes(reg))

    def write_reg_config(self, reg: ConfigReg) -> None:
        self.write_reg(Address.CONFIG, bytes(reg))

    def close(self):
        self.backend.close()
