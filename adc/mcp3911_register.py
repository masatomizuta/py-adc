#!/usr/bin/env python3

"""
MCP3911 Register Definitions
Reference: DS20002286C
"""

import ctypes
from enum import IntEnum

from .register import Register


class Address(IntEnum):
    """Register Address"""

    CHANNEL0 = 0x00
    """Channel 0 ADC 24-bit Data <23:0>, MSB first"""
    CHANNEL1 = 0x03
    """Channel 1 ADC 24-bit Data <23:0>, MSB first"""
    MOD = 0x06
    """Modulator Output Register for both ADC channels"""
    PHASE = 0x07
    """Phase Delay Configuration Register"""
    GAIN = 0x09
    """Gain and Boost Configuration Register"""
    STATUSCOM = 0x0A
    """Status and Communication Register"""
    CONFIG = 0x0C
    """Configuration Register"""
    OFFCAL_CH0 = 0x0E
    """Offset Correction Register - Channel 0"""
    GAINCAL_CH0 = 0x11
    """Gain Correction Register - Channel 0"""
    OFFCAL_CH1 = 0x14
    """Offset Correction Register - Channel 1"""
    GAINCAL_CH1 = 0x17
    """Gain Correction Register - Channel 1"""
    VREFCAL = 0x1A
    """Internal Voltage reference Temperature Coefficient Adjustment Register"""


class GainReg(Register):
    """Gain and Boost Configuration Register"""
    _fields_ = [('boost', ctypes.c_uint8, 2),
                ('pga_ch1', ctypes.c_uint8, 3),
                ('pga_ch0', ctypes.c_uint8, 3)]

    class Boost(IntEnum):
        """Bias Current Selection"""
        x2 = 0b11
        """Both channels have current x 2"""
        x1 = 0b10
        """Both channels have current x 1 (DEFAULT)"""
        x0_66 = 0b01
        """Both channels have current x 0.66"""
        x0_5 = 0b00
        """Both channels have current x 0.5"""

    class Pga(IntEnum):
        """PGA Setting"""
        x32 = 0b101
        x16 = 0b100
        x8 = 0b011
        x4 = 0b010
        x2 = 0b001
        x1 = 0b000
        """(DEFAULT)"""

    def __init__(self, boost=Boost.x1, pga_ch1=Pga.x1, pga_ch0=Pga.x1):
        super().__init__(boost, pga_ch1, pga_ch0)


class StatusComReg(Register):
    """Status and Communication Register"""
    _fields_ = [('modout', ctypes.c_uint8, 2),
                ('_unimplemented1', ctypes.c_uint8, 1),
                ('dr_hiz', ctypes.c_uint8, 1),
                ('drmode', ctypes.c_uint8, 2),
                ('drstatus', ctypes.c_uint8, 2),
                ('read', ctypes.c_uint8, 2),
                ('write', ctypes.c_uint8, 1),
                ('width', ctypes.c_uint8, 2),
                ('en_offcal', ctypes.c_uint8, 1),
                ('en_gaincal', ctypes.c_uint8, 1),
                ('_unimplemented2', ctypes.c_uint8, 1)]

    class ModOut(IntEnum):
        """Modulator Output Setting for MDAT Pins"""
        both = 0b11
        """Both CH0 and CH1 modulator outputs are present on MDAT1 and MDAT0 pins, 
        both SINC filters are off and no data ready pulse is present."""
        ch1 = 0b10
        """CH1 ADC Modulator output present on MDAT1 pin,
        SINC filter on Channel 1 is off and data ready pulse from Channel 1 is not present on DR pin."""
        ch0 = 0b01
        """CH0 ADC Modulator output present on MDAT0 pin,
        SINC filter on Channel 0 is off and data ready pulse from Channel 0 is not present on DR pin."""
        off = 0b00
        """No Modulator output is enabled,
        SINC filters are on and data ready pulses are present on DR pin for both channels (DEFAULT)"""

    class DR_HIZ(IntEnum):
        """Data Ready Pin Inactive State Control"""
        logic_high = 1
        """The DR pin state is a logic high when data is NOT ready"""
        high_z = 0
        """The DR pin state is high-impedance when data is NOT ready (DEFAULT)"""

    class DRMode(IntEnum):
        """Data Ready Pin (DR) mode configuration bits"""
        both = 0b11
        """Both Data Ready pulses from CH0 and CH1 are output on DR pin."""
        ch1 = 0b10
        """Data Ready pulses from CH1 ADC are output on DR pin. 
        Data ready pulses from CH0 are not present on the DR pin."""
        ch0 = 0b01
        """Data Ready pulses from CH0 ADC are output on DR pin.
        Data ready pulses from CH1 are not present on the DR pin."""
        lag = 0b00
        """Data Ready pulses from the lagging ADC between the two are output on DR pin.
        The lagging ADC depends on the PHASE register and on the OSR (DEFAULT)."""

    class DRStatus(IntEnum):
        """Data Ready Status"""
        none = 0b11
        """ADC Channel 1 and Channel 0 data not ready (DEFAULT)"""
        ch0 = 0b10
        """ADC Channel 1 data not ready, ADC Channel 0 data ready"""
        ch1 = 0b01
        """ADC Channel 0 data not ready, ADC Channel 1 data ready"""
        both = 0b00
        """ADC Channel 1 and Channel 0 data ready"""

    class Read(IntEnum):
        """Address Loop Setting"""
        all = 0b11
        """Address counter incremented, cycle through entire register set"""
        types = 0b10
        """Address counter loops on register types (DEFAULT)"""
        groups = 0b01
        """Address counter loops on register groups"""
        off = 0b00
        """Address not incremented, continually read single register"""

    class Write(IntEnum):
        """Address Loop Setting for Write mode"""
        on = 1
        """Address counter loops on entire register map (DEFAULT)"""
        off = 0
        """Address not incremented, continually write same single register"""

    class Width(IntEnum):
        """ADC Channel output data word width"""
        both_ch_24bit = 0b11
        """Both channels are in 24-bit mode(DEFAULT)"""
        ch1_24bit_ch0_16bit = 0b10
        """Channel1 in 24-bit mode, Channel0 in 16-bit mode"""
        ch1_16bit_ch0_24bit = 0b01
        """Channel1 in 16-bit mode, Channel0 in 24-bit mode"""
        both_ch_16bit = 0b00
        """Both channels are in 16-bit mode"""

    class EN_OffCal(IntEnum):
        """Enables or disables the 24-bit digital offset calibration on both channels"""
        enabled = 1
        """Enabled; this mode does not add any group delay"""
        disabled = 0
        """Disabled (DEFAULT)"""

    class EN_GainCal(IntEnum):
        """Enables or disables the 24-bit digital offset calibration on both channels"""
        enabled = 1
        """Enabled; this mode adds a group delay on both channels of 24 DMCLK periods.
        All data ready pulses are delayed by 24 clock periods compared to the mode with EN_GAINCAL = 0"""
        disabled = 0
        """Disabled (DEFAULT)"""

    def __init__(self, modout=ModOut.off, dr_hiz=DR_HIZ.high_z, drmode=DRMode.lag, drstatus=DRStatus.none,
                 read=Read.types, write=Write.on, width=Width.both_ch_24bit, en_offcal=EN_OffCal.disabled,
                 en_gaincal=EN_GainCal.disabled):
        super().__init__(modout, 0, dr_hiz, drmode, drstatus, read, write, width, en_offcal, en_gaincal, 0)


class ConfigReg(Register):
    """Configuration Register"""
    _fields_ = [('pre', ctypes.c_uint8, 2),
                ('osr', ctypes.c_uint8, 3),
                ('dither', ctypes.c_uint8, 2),
                ('az_freq', ctypes.c_uint8, 1),
                ('reset', ctypes.c_uint8, 2),
                ('shutdown', ctypes.c_uint8, 2),
                ('_unimplemented1', ctypes.c_uint8, 1),
                ('vrefext', ctypes.c_uint8, 1),
                ('clkext', ctypes.c_uint8, 1),
                ('_unimplemented2', ctypes.c_uint8, 1)]

    class Pre(IntEnum):
        """Analog Master Clock (AMCLK) Prescaler Value"""
        pre8 = 0b11
        pre4 = 0b10
        pre2 = 0b01
        pre1 = 0b00
        """(DEFAULT)"""

    class Osr(IntEnum):
        """Oversampling Ratio for Delta-Sigma A/D Conversion (ALL CHANNELS, fd/fS)"""
        osr4096 = 0b111
        osr2048 = 0b110
        osr1024 = 0b101
        osr512 = 0b100
        osr256 = 0b011
        """(DEFAULT)"""
        osr128 = 0b010
        osr64 = 0b001
        osr32 = 0b000

    class Dither(IntEnum):
        """Control for dithering circuit for idle tones cancellation and improved THD"""
        both = 0b11
        """Dithering ON, both channels, Strength = Maximum(MCP3901 Equivalent) - (DEFAULT)"""
        ch1 = 0b10
        """Dithering ON, both channels, Strength = Medium"""
        ch0 = 0b01
        """Dithering ON, both channels, Strength = Minimum"""
        off = 0b00
        """Dithering turned OFF"""

    class AzFreq(IntEnum):
        """Auto-zero frequency setting"""
        high = 1
        """Auto-zeroing algorithm running at higher speed"""
        low = 0
        """Auto-zeroing algorithm running at lower speed (Default)"""

    class Reset(IntEnum):
        """Reset mode setting for ADCs"""
        both = 0b11
        """Both CH0 and CH1 ADC are in reset mode"""
        ch1 = 0b10
        """CH1 ADC in Reset mode"""
        ch0 = 0b01
        """CH0 ADC in Reset mode"""
        neither = 0b00
        """Neither ADC in Reset mode (default)"""

    class Shutdown(IntEnum):
        """Shutdown mode setting for ADCs"""
        both = 0b11
        """Both CH0 and CH1 ADC in Shutdown"""
        ch1 = 0b10
        """CH1 ADC in Shutdown"""
        ch0 = 0b01
        """CH0 ADC in Shutdown"""
        neither = 0b00
        """Neither Channel in Shutdown (default)"""

    class VrefExt(IntEnum):
        """Internal Voltage Reference Shutdown Control"""
        external = 1
        """Internal Voltage Reference Disabled"""
        internal = 0
        """Internal Voltage Reference Enabled (Default)"""

    class ClkExt(IntEnum):
        """Internal Clock selection bits"""
        external = 1
        """External clock drive by MCU on OSC1 pin (crystal oscillator disabled,
        no internal power consumption) (Default)"""
        crystal = 0
        """Crystal oscillator is enabled. A crystal must be placed between OSC1 and OSC2 pins."""

    def __init__(self, pre=Pre.pre1, osr=Osr.osr256, dither=Dither.both, az_freq=AzFreq.low,
                 reset=Reset.neither, shutdown=Shutdown.neither, vrefext=VrefExt.internal, clkext=ClkExt.external):
        super().__init__(pre, osr, dither, az_freq, reset, shutdown, 0, vrefext, clkext, 0)
