#!/usr/bin/env python3

import statistics
import time

import pigpio

import adc
import adc.mcp3911_register as reg

pi = pigpio.pi()
spi = pi.spi_open(0, 250000)

ad = adc.MCP3911(adc.SPI_pigpio(pi, spi))

print(ad.read_reg_status_com().to_string())

ad.write_reg_gain(reg.GainReg(
    boost=reg.GainReg.Boost.x2
))

ad.write_reg_status_com(reg.StatusComReg(
    read=reg.StatusComReg.Read.groups,
    width=reg.StatusComReg.Width.both_ch_16bit
))

print(ad.read_reg_status_com().to_string())

ad.write_reg_config(reg.ConfigReg(
    pre=reg.ConfigReg.Pre.pre1,
    osr=reg.ConfigReg.Osr.osr512,
    clkext=reg.ConfigReg.ClkExt.crystal
))

time.sleep(0.1)

start = time.time()
array = ad.read_data_array(15625, ch=0, width=16)
elapsed_time = time.time() - start

avg = statistics.mean(array)
minimum = min(array)
maximum = max(array)
st_dev = statistics.stdev(array)
st_dev_pct = st_dev / avg * 100

print(array[0:20])
print(f'average: {avg}')
print(f'min: {minimum}')
print(f'max: {maximum}')
print(f'standard dev: {st_dev}')
print(f'standard dev%: {st_dev_pct}')
print(f'elapsed: {elapsed_time} sec')

ad.close()
pi.stop()
