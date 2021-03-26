#!/usr/bin/env python3

import statistics
import time

import pigpio

import adc.mcp3911_register as reg
from adc import MCP3911, SPI_pigpio

pi = pigpio.pi()
SPI_CH = 0
SPI_BAUD = 1000000
ADC_DR_PIN = 13

ad = MCP3911(SPI_pigpio(pi, SPI_CH, SPI_BAUD, ADC_DR_PIN))

ad.write_reg_gain(reg.GainReg(
    boost=reg.GainReg.Boost.x2
))

ad.write_reg_status_com(reg.StatusComReg(
    read=reg.StatusComReg.Read.groups,
    width=reg.StatusComReg.Width.both_ch_16bit
))

ad.write_reg_config(reg.ConfigReg(
    pre=reg.ConfigReg.Pre.pre1,
    osr=reg.ConfigReg.Osr.osr128,
    clkext=reg.ConfigReg.ClkExt.crystal
))

print(ad.read_reg_gain().to_string())
print(ad.read_reg_status_com().to_string())
print(ad.read_reg_config().to_string())

time.sleep(0.1)

start = time.time()
array = ad.read_data_array(15625, ch=0, width=16)
elapsed_time = time.time() - start

avg = statistics.mean(array)
minimum = min(array)
maximum = max(array)
st_dev = statistics.stdev(array)
st_dev_pct = st_dev / avg * 100

print(array[:10])
print("average: {}".format(avg))
print("min: {}".format(minimum))
print("max: {}".format(maximum))
print("standard dev: {}".format(st_dev))
print("standard dev%: {}".format(st_dev_pct))
print("elapsed: {} sec".format(elapsed_time))

ad.close()
pi.stop()
