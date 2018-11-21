#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod


class Backend(object, metaclass=ABCMeta):
    """
    Abstract backend
    """

    @abstractmethod
    def transfer(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def get_data(self, addr: int, byte_width: int, sample_len: int) -> [int]:
        pass

    @abstractmethod
    def close(self):
        pass
