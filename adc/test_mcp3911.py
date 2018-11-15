#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from adc.mcp3911 import MCP3911
from adc.mcp3911_register import *
from adc.backends.backend import Backend


class TestMCP3911(unittest.TestCase):

    def setUp(self):
        self.backend = unittest.mock.create_autospec(spec=Backend)
        self.ad = MCP3911(self.backend)

    def test_write_reg_gain(self):
        gain = GainReg(boost=GainReg.Boost.x2, pga_ch0=GainReg.Pga.x8, pga_ch1=GainReg.Pga.x16)
        self.ad.write_reg_gain(gain)
        self.backend.transfer.assert_called_once_with(bytes([Address.GAIN << 1]) + bytes(gain))

    def test_write_reg_status_com(self):
        status = StatusComReg(modout=StatusComReg.ModOut.ch0)
        self.ad.write_reg_status_com(status)
        self.backend.transfer.assert_called_once_with(bytes([Address.STATUSCOM << 1]) + bytes(status))

    def test_write_reg_config(self):
        config = ConfigReg(pre=ConfigReg.Pre.pre8)
        self.ad.write_reg_config(config)
        self.backend.transfer.assert_called_once_with(bytes([Address.CONFIG << 1]) + bytes(config))
