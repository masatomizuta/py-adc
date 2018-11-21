#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <sys/mman.h>

#ifdef __linux__
#include <linux/spi/spidev.h>
#endif

#include <Python.h>

#define BLOCK_SIZE  4096
#define GPIO_LEVEL_OFFSET  13  // GPLEV0 Pin Level register

uint32_t *gpio_init() {
    int fd = open("/dev/gpiomem", O_RDWR | O_SYNC);
    if (fd < 0) {
        return NULL;
    }

    void *gpio_mmap = mmap(NULL, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (gpio_mmap == MAP_FAILED) {
        return NULL;
    }

    close(fd);
    return (uint32_t *) gpio_mmap;
}

void gpio_set_input(uint32_t *gpio_mmap, int pin_no) {
    int block_addr = (pin_no / 10);
    long setting = ~(0x7 << ((pin_no % 10) * 3));

    *(gpio_mmap + block_addr) &= setting;
}

int gpio_read(const uint32_t *gpio_mmap, int pin_no) {
    int block_addr = GPIO_LEVEL_OFFSET + (pin_no / 32);
    long mask = (0x1 << (pin_no % 32));
    long reading = *(gpio_mmap + block_addr) & mask;
    return (int) (reading != 0);
}

#ifdef __linux__

int spi_open(uint8_t ch, unsigned int baud) {
    char mode = SPI_MODE_0;
    char bits = 8;

    char dev[32];
    sprintf(dev, "/dev/spidev0.%d", ch);

    int fd = open(dev, O_RDWR);
    if (fd < 0) {
        return -1;
    }

    if (ioctl(fd, SPI_IOC_WR_MODE, &mode) < 0) {
        close(fd);
        return -2;
    }

    if (ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits) < 0) {
        close(fd);
        return -3;
    }

    if (ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &baud) < 0) {
        close(fd);
        return -4;
    }

    return fd;
}

int spi_xfer(int fd, unsigned int baud, char *txbuf, char *rxbuf, unsigned int length) {
    struct spi_ioc_transfer spi;
    memset(&spi, 0, sizeof(spi));

    spi.tx_buf = (unsigned long) txbuf;
    spi.rx_buf = (unsigned long) rxbuf;
    spi.len = length;
    spi.speed_hz = baud;
    spi.delay_usecs = 0;
    spi.bits_per_word = 8;
    spi.cs_change = 0;

    return ioctl(fd, SPI_IOC_MESSAGE(1), &spi);
}

#else

int spi_open(uint8_t ch, unsigned int baud) {
    return -1;
}

int spi_xfer(int fd, unsigned int baud, char *txbuf, char *rxbuf, unsigned int length) {
    return -1;
}

#endif  // __linux__

int raw_get_data(uint8_t spi_ch, uint32_t spi_baud, uint8_t dr_pin, uint8_t addr, uint8_t byte_width,
                 uint32_t sample_len, uint32_t *samples) {
    uint32_t *gpio_mmap = gpio_init();
    if (gpio_mmap == NULL) {
        printf("Failed to open gpio\n");
        return 1;
    }

    gpio_set_input(gpio_mmap, dr_pin);

    int fd = spi_open(spi_ch, spi_baud);
    if (fd < 0) {
        printf("Failed to open spi\n");
        return 1;
    }

    char txbuf[4];
    char rxbuf[4];
    txbuf[0] = (char) (addr << 1 | 1);

    if (byte_width == 2) {
        for (uint32_t i = 0; i < sample_len; i++) {
            while (gpio_read(gpio_mmap, dr_pin)) {}
            spi_xfer(fd, spi_baud, txbuf, rxbuf, 3);
            samples[i] = ((uint32_t) rxbuf[1] << 8) | rxbuf[2];
        }
    } else if (byte_width == 3) {
        for (uint32_t i = 0; i < sample_len; i++) {
            while (gpio_read(gpio_mmap, dr_pin)) {}
            spi_xfer(fd, spi_baud, txbuf, rxbuf, 4);
            samples[i] = ((uint32_t) rxbuf[1] << 16) | ((uint32_t) rxbuf[2] << 8) | rxbuf[3];
        }
    } else {
        printf("Unsupported bytes width\n");
        close(fd);
        return 1;
    }

    close(fd);
    return 0;
}

static PyObject *get_data(PyObject *self, PyObject *args) {
    uint8_t spi_ch;
    uint32_t spi_baud;
    uint8_t dr_pin;
    uint8_t addr;
    uint8_t byte_width;
    uint32_t sample_len;

    if (!PyArg_ParseTuple(args, "bIbbbI", &spi_ch, &spi_baud, &dr_pin, &addr, &byte_width, &sample_len)) {
        return NULL;
    }

    PyObject *py_list = PyList_New(sample_len);
    if (py_list == NULL) {
        printf("PyList_New() failed.");
        return NULL;
    }

    uint32_t *samples = malloc(sizeof(uint32_t) * sample_len);
    if (samples == NULL) {
        printf("malloc() failed.");
        Py_DECREF(py_list);
        return NULL;
    }

    if (raw_get_data(spi_ch, spi_baud, dr_pin, addr, byte_width, sample_len, samples)) {
        printf("raw_get_data() failed.");
        Py_DECREF(py_list);
        free(samples);
        return NULL;
    }

    for (uint32_t i = 0; i < sample_len; i++) {
        PyList_SetItem(py_list, i, Py_BuildValue("I", samples[i]));
    }

    free(samples);

    return py_list;
}

static PyMethodDef methods[] = {
        {"get_data", (PyCFunction) get_data, METH_VARARGS, "Get adc data."},
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT,
        "spi_rpi",
        NULL,
        -1,
        methods
};

PyMODINIT_FUNC PyInit_spi_rpi(void) {
    return PyModule_Create(&module);
}
