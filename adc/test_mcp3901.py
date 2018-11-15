#!/usr/bin/env python3

import unittest
from unittest.mock import Mock

from adc.mcp3901 import MCP3901
from adc.mcp3901_register import *
from adc.backends.backend import Backend


class TestMCP3901(unittest.TestCase):

    def setUp(self):
        self.backend = unittest.mock.create_autospec(spec=Backend)
        self.ad = MCP3901(self.backend)

    def test_write_reg_gain(self):
        gain = GainReg(boost=GainReg.Boost.ch0, pga_ch0=GainReg.Pga.x2, pga_ch1=GainReg.Pga.x4)
        self.ad.write_reg_gain(gain)
        self.backend.transfer.assert_called_once_with(bytes([Address.GAIN << 1]) + bytes(gain))

    def test_write_reg_status_com(self):
        status = StatusComReg(read=StatusComReg.Read.all)
        self.ad.write_reg_status_com(status)
        self.backend.transfer.assert_called_once_with(bytes([Address.STATUS_COM << 1]) + bytes(status))

    def test_write_reg_config1(self):
        config = Config1Reg(prescale=Config1Reg.Prescale.pre8)
        self.ad.write_reg_config1(config)
        self.backend.transfer.assert_called_once_with(bytes([Address.CONFIG1 << 1]) + bytes(config))

    def test_write_reg_config2(self):
        config = Config2Reg(reset=Config2Reg.Reset.ch0)
        self.ad.write_reg_config2(config)
        self.backend.transfer.assert_called_once_with(bytes([Address.CONFIG2 << 1]) + bytes(config))
