# py-adc

py-adc is a Python library to interface with ADC devices.

## Supported Devices

- MCP3901
- MCP3911

## Testing

Build extension module first.

```bash
python3 setup.py build_ext -i
python3 example_pigpio.py
```

## Note

When SPI does not work, try to reload spi_bcm2835 kernel module.

```bash
sudo rmmod spi_bcm2835
sudo modprobe spi_bcm2835
```
