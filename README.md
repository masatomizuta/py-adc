# py-adc

py-adc is a Python library to interface with ADC devices.

## Supported Devices

- MCP3901
- MCP3911

## Install

```shell
pip3 install git+https://github.com/masatomizuta/py-adc
```

## Development

Build the extension module first.

```shell
python3 setup.py build_ext -i
```

## Note

- Enable SPI on a Raspberry Pi board:

```shell
sudo raspi-config nonint do_spi 0
```

- Start pigpiod:

```shell
sudo systemctl start pigpiod
```
