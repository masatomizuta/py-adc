#!/usr/bin/env python3

import unittest

import adc.mcp3901_register as reg


class TestMCP3901Register(unittest.TestCase):

    def test_GainReg(self):
        bits = 0
        for f in reg.GainReg._fields_:
            bits += f[2]
        self.assertEqual(bits, 8)
        self.assertEqual(len(bytes(reg.GainReg())), 1)

    def test_StatusComReg(self):
        bits = 0
        for f in reg.StatusComReg._fields_:
            bits += f[2]
        self.assertEqual(bits, 8)
        self.assertEqual(len(bytes(reg.StatusComReg())), 1)

    def test_Config1Reg(self):
        bits = 0
        for f in reg.Config1Reg._fields_:
            bits += f[2]
        self.assertEqual(bits, 8)
        self.assertEqual(len(bytes(reg.Config1Reg())), 1)

    def test_Config2Reg(self):
        bits = 0
        for f in reg.Config2Reg._fields_:
            bits += f[2]
        self.assertEqual(bits, 8)
        self.assertEqual(len(bytes(reg.Config2Reg())), 1)
