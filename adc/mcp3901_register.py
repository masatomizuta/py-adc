#!/usr/bin/env python3

"""
MCP3901 Register Definitions
Reference: DS22192C
"""

import ctypes
from enum import IntEnum

from .register import Register


class Address(IntEnum):
    """Register Address"""

    DATA_CH0 = 0x00
    """Channel 0 ADC Data <23:0>, MSB First"""
    DATA_CH1 = 0x03
    """Channel 1 ADC Data <23:0>, MSB First"""
    MOD = 0x06
    """Delta Sigma Modulators Output Register"""
    PHASE = 0x07
    """Phase Delay Configuration Register"""
    GAIN = 0x08
    """Gain Configuration Register"""
    STATUS_COM = 0x09
    """Status / Communication Register"""
    CONFIG1 = 0x0A
    """Configuration Register 1"""
    CONFIG2 = 0x0B
    """Configuration Register 2"""


class GainReg(Register):
    """Gain Configuration Register"""
    _fields_ = [('pga_ch1', ctypes.c_uint8, 3),
                ('boost', ctypes.c_uint8, 2),
                ('pga_ch0', ctypes.c_uint8, 3)]

    class Pga(IntEnum):
        """PGA Setting bits"""
        x32 = 0b101
        x16 = 0b100
        x8 = 0b011
        x4 = 0b010
        x2 = 0b001
        x1 = 0b000
        """(DEFAULT)"""

    class Boost(IntEnum):
        """Current Scaling for High-Speed Operation bits"""
        both = 0b11
        """Both channels have current x 2"""
        ch1 = 0b10
        """Channel 1 has current x 2"""
        ch0 = 0b01
        """Channel 0 has current x 2"""
        neither = 0b00
        """Neither channel has current x 2 (DEFAULT)"""

    def __init__(self, pga_ch1=Pga.x1, boost=Boost.neither, pga_ch0=Pga.x1):
        super().__init__(pga_ch1, boost, pga_ch0)


class StatusComReg(Register):
    """Status and Communication Register"""
    _fields_ = [('read', ctypes.c_uint8, 2),
                ('dr_lty', ctypes.c_uint8, 1),
                ('dr_hizn', ctypes.c_uint8, 1),
                ('drmode', ctypes.c_uint8, 2),
                ('drstatus', ctypes.c_uint8, 2)]

    class Read(IntEnum):
        """Address Loop Setting bits"""
        all = 0b11
        """Address counter loops on entire register map"""
        types = 0b10
        """Address counter loops on register types (default)"""
        groups = 0b01
        """Address counter loops on register groups"""
        off = 0b00
        """Address not incremented, continually read same single register"""

    class DR_Lty(IntEnum):
        """Data Ready Latency Control bit"""
        off = 1
        """“No Latency” Conversion, DR pulses after 3 DRCLK periods (default)"""
        on = 0
        """Unsettled Data is available after every DRCLK period"""

    class DR_HIZn(IntEnum):
        """Data Ready Pin Inactive State Control bit"""
        logic_high = 1
        """The data ready pin default state is a logic high when data is NOT ready"""
        high_z = 0
        """The data ready pin default state is high-impedance when data is NOT ready (default)"""

    class DRMode(IntEnum):
        """Data Ready Pin (DR) Control bits"""
        both = 0b11
        """Both Data Ready pulses from ADC0 and ADC Channel 1 are output on the DR pin."""
        ch1 = 0b10
        """Data Ready pulses from ADC Channel 1 are output on the DR pin.
        DR from ADC Channel 0 are not present on the pin."""
        ch0 = 0b01
        """Data Ready pulses from ADC Channel 0 are output on the DR pin.
        DR from ADC Channel 1 are not present on the pin."""
        lag = 0b00
        """Data Ready pulses from the lagging ADC between the two are output on the DR pin.
        The lagging ADC selection depends on the PHASE register and on the OSR (default)."""

    class DRStatus(IntEnum):
        """Data Ready Status bits"""
        none = 0b11
        """ADC Channel 1 and Channel 0 data is not ready (default)"""
        ch0 = 0b10
        """ADC Channel 1 data is not ready, ADC Channel 0 data is ready"""
        ch1 = 0b01
        """ADC Channel 0 data is not ready, ADC Channel 1 data is ready"""
        both = 0b00
        """ADC Channel 1 and Channel 0 data is ready"""

    def __init__(self, read=Read.types, dr_lty=DR_Lty.off, dr_hizn=DR_HIZn.high_z, drmode=DRMode.lag,
                 drstatus=DRStatus.none):
        super().__init__(read, dr_lty, dr_hizn, drmode, drstatus)


class Config1Reg(Register):
    """Configuration Register 1"""
    _fields_ = [('prescale', ctypes.c_uint8, 2),
                ('osr', ctypes.c_uint8, 2),
                ('width', ctypes.c_uint8, 2),
                ('modout', ctypes.c_uint8, 2)]

    class Prescale(IntEnum):
        """Internal Master Clock (AMCLK) Prescaler Value bits"""
        pre8 = 0b11
        pre4 = 0b10
        pre2 = 0b01
        pre1 = 0b00
        """(DEFAULT)"""

    class Osr(IntEnum):
        """Oversampling Ratio for Delta-Sigma A/D Conversion bits (all channels, DMCLK/DRCLK)"""
        osr256 = 0b11
        osr128 = 0b10
        osr64 = 0b01
        """(DEFAULT)"""
        osr32 = 0b00

    class Width(IntEnum):
        """ADC Channel Output Data Word Width bits"""
        w24 = 1
        """24-bit mode"""
        w16 = 0
        """16-bit mode (default)"""

    class ModOut(IntEnum):
        """Modulator Output Setting for MDAT Pins bits"""
        both = 0b11
        """Both CH0 and CH1 modulator outputs present on MDAT1 and MDAT0 pins"""
        ch1 = 0b10
        """CH1 ADC modulator output present on MDAT1 pin"""
        ch0 = 0b01
        """CH0 ADC modulator output present on MDAT0 pin"""
        off = 0b00
        """No modulator output is enabled (default)"""

    def __init__(self, prescale=Prescale.pre1, osr=Osr.osr64, width=Width.w16, modout=ModOut.off):
        super().__init__(prescale, osr, width, modout)


class Config2Reg(Register):
    """Configuration Register 2"""
    _fields_ = [('reset', ctypes.c_uint8, 2),
                ('shutdown', ctypes.c_uint8, 2),
                ('dither', ctypes.c_uint8, 2),
                ('vrefext', ctypes.c_uint8, 1),
                ('clkext', ctypes.c_uint8, 1)]

    class Reset(IntEnum):
        """Reset Mode Setting for ADCs bits"""
        both = 0b11
        """Both CH0 and CH1 ADC are in Reset mode"""
        ch1 = 0b10
        """CH1 ADC in Reset mode"""
        ch0 = 0b01
        """CH0 ADC in Reset mode"""
        neither = 0b00
        """Neither Channel in Reset mode (default)"""

    class Shutdown(IntEnum):
        """Shutdown Mode Setting for ADCs bits"""
        both = 0b11
        """Both CH0 and CH1 ADC are in Shutdown"""
        ch1 = 0b10
        """CH1 ADC is in shutdown"""
        ch0 = 0b01
        """CH0 ADC is in shutdown"""
        neither = 0b00
        """Neither Channel is in shutdown (default)"""

    class Dither(IntEnum):
        """Control for Dithering Circuit bits"""
        both = 0b11
        """Both CH0 and CH1 ADC have dithering circuit applied (default)"""
        ch1 = 0b10
        """Only CH1 ADC has dithering circuit applied"""
        ch0 = 0b01
        """Only CH0 ADC has dithering circuit applied"""
        neither = 0b00
        """Neither Channel has dithering circuit applied"""

    class VrefExt(IntEnum):
        """Internal Voltage Reference Shutdown Control bit"""
        external = 1
        """Internal voltage reference disabled,
        an external voltage reference must be placed between REFIN+/OUT and REFIN-"""
        internal = 0
        """Internal voltage reference enabled (default)"""

    class ClkExt(IntEnum):
        """Clock Mode bit"""
        external = 1
        """External Clock mode (internal oscillator disabled and bypassed – lower power)"""
        crystal = 0
        """XT mode – A crystal must be placed between OSC1/OSC2 (default)"""

    def __init__(self, reset=Reset.neither, shutdown=Shutdown.neither, dither=Dither.both, vrefext=VrefExt.internal,
                 clkext=ClkExt.crystal):
        super().__init__(reset, shutdown, dither, vrefext, clkext)
