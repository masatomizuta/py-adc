#!/usr/bin/env python

from setuptools import setup

setup(
    name='py-adc',
    version='0.1.0',
    description='Python library for ADC devices',
    author='Masato Mizuta',
    author_email='mst.mizuta@gmail.com',
    url='https://github.com/masatomizuta/py-adc/',
    packages=['adc', 'adc.backends'],
    install_requires=[
        'pigpio'
    ],
    keywords='ADC, MCP3901, MCP3911'
)
