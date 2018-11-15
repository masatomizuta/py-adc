#!/usr/bin/env python3

import unittest

import adc.mcp3911_register as reg


class TestMCP3911Register(unittest.TestCase):

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
        self.assertEqual(bits, 16)
        self.assertEqual(len(bytes(reg.StatusComReg())), 2)

        val = reg.StatusComReg(modout=reg.StatusComReg.ModOut.ch0)
        self.assertEqual(val.modout, reg.StatusComReg.ModOut.ch0)

        val.modout = reg.StatusComReg.ModOut.ch1
        self.assertEqual(val.modout, reg.StatusComReg.ModOut.ch1)

    def test_ConfigReg(self):
        bits = 0
        for f in reg.ConfigReg._fields_:
            bits += f[2]
        self.assertEqual(bits, 16)
        self.assertEqual(len(bytes(reg.ConfigReg())), 2)
