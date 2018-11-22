#!/usr/bin/env python3

import ctypes


class Register(ctypes.BigEndianStructure):
    _pack_ = 1

    def to_string(self) -> str:
        s = ""
        for field in self._fields_:
            if field[0][0] != "_":
                s += "{}: {:b}\n".format(field[0], getattr(self, field[0]))
        return s

    @classmethod
    def from_bytes(cls, data: bytes):
        r = cls()
        ctypes.memmove(ctypes.addressof(r), data, len(data))
        return r
