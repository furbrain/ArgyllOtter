#!/usr/bin/env python3
import os

import numpy as np

if os.path.isdir("/home/pi"):
    SETTINGS_DIR = "/home/pi/settings/"
else:
    SETTINGS_DIR = "/home/phil/shetty_settings/"


class Settings:
    def __init__(self):
        self.default()
        self.load()

    def default(self):
        raise NotImplementedError

    @classmethod
    def filename(cls):
        return SETTINGS_DIR + cls.__name__ + ".npz"

    def load(self):
        try:
            data = np.load(self.filename(), allow_pickle=True)
        except IOError:
            return
        for k, v in data.items():
            if k in self.__dict__:
                setattr(self, k, v)

    def save(self):
        # exceptions deliberately un-caught here
        saveable = {k: v for k, v in self.__dict__.items() if k[0] != "_"}
        np.savez(self.filename(), **saveable)
        os.chmod(self.filename(), 0o666)


if __name__ == "__main__":
    class TestSettings(Settings):
        def default(self):
            self.a = 1
            self.b = 2


    try:
        os.remove(TestSettings.filename())
    except IOError:
        pass
    test1 = TestSettings()
    print("first use")
    print(test1.__dict__)
    test1.a = np.array([1, 2, 3, 4])
    test1.b = {"fred": "jane"}
    test1.c = "error"
    print("after changes")
    print(test1.__dict__)
    test1.save()
    del test1
    print("test2")
    test2 = TestSettings()
    print(test2.__dict__)
