#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod


class Backend(object, metaclass=ABCMeta):
    """
    Abstract backend
    """

    @abstractmethod
    def transfer(self, data: bytes) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()
