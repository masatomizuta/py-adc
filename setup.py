#!/usr/bin/env python

from setuptools import Extension, setup

setup(
    name='py-adc',
    version='0.1.1',
    description='Python library for ADC devices',
    author='Masato Mizuta',
    author_email='mst.mizuta@gmail.com',
    url='https://github.com/masatomizuta/py-adc/',
    packages=['adc', 'adc.backends'],
    ext_modules=[Extension('adc.backends.ext.spi_rpi', ['adc/backends/ext/spi_rpi.c'])],
    install_requires=[
        'pigpio'
    ],
    keywords='ADC, MCP3901, MCP3911'
)
