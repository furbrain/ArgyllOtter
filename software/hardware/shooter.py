#!/usr/bin/env python3
import asyncio

import gpiozero
import numpy as np
import smbus

import settings
from util import logged
from . import orientation
from . import servo

BMP388_ADDRESS = 0x77
CAL_RANGE = (-100, 900, 50)


class Shooter:
    def __init__(self):
        self.pressure = Pressure()
        self.pump = Pump()
        self.pointer = Pointer()
        self.barrel = Barrel()

    async def finish(self):
        self.pump.off()
        self.pointer.off()
        self.barrel.servo.off()


class Pressure:
    def __init__(self, bus=None, address=BMP388_ADDRESS):
        if bus is None:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = bus
        self.address = address
        self.bus.write_byte_data(self.address, 0x1b, 0x31)
        self.bus.write_byte_data(self.address, 0x1c, 0x00)
        self.bus.write_byte_data(self.address, 0x1d, 0x01)

    @logged
    def get_pressure(self):
        try:
            data = self.bus.read_i2c_block_data(self.address, 0x04, 0x03)
            result = data[0] + data[1] * 0x100 + data[2] * 0x10000
            result *= 0.016
        except IOError:
            result = None
        return result


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class BarrelPositions(settings.Settings):
    def default(self):
        self.range = np.arange(*CAL_RANGE)
        self.up = self.range[:]
        self.down = self.range[:]

    def get_up_position(self, angle):
        return np.interp(angle, self.up, self.range)

    def get_down_position(self, angle):
        return np.interp(angle, self.down, self.range)


class Barrel:
    def __init__(self, bus=None):
        self.servo = servo.Servo(inverted=True)
        self.position = -10
        self.orientation = orientation.Orientation(bus=bus, address=0x69)
        self.angle = self.orientation.get_angle()
        self.cal = BarrelPositions()

    @logged
    def get_angle(self):
        return self.orientation.get_angle()

    @logged
    def set_pos(self, pos):
        self.position = pos
        self.servo.set_pos(pos)

    @logged
    def get_pos(self):
        return self.position

    @logged
    def set_angle_quick(self, angle):
        cur_angle = self.orientation.get_angle()
        if angle > cur_angle + 5:
            self.servo.set_pos(self.cal.get_up_position(angle))
        elif angle < cur_angle - 5:
            self.servo.set_pos(self.cal.get_down_position(angle))

    @logged
    async def set_angle(self, angle):
        cur_angle = self.orientation.get_angle()
        self.set_angle_quick(angle)
        await asyncio.sleep(0.3)
        on_pos_count = 0
        while True:
            if abs(angle - cur_angle) < 0.5:
                on_pos_count += 1
                if on_pos_count >= 2:
                    break
            else:
                on_pos_count = 0
                if angle < cur_angle:
                    self.position -= 2
                else:
                    self.position += 2
                self.servo.set_pos(self.position)
            await asyncio.sleep(0.04)
            cur_angle = self.orientation.get_angle()
        print("set_angle finished")


# noinspection PyPep8Naming
def Pointer():
    return gpiozero.LED(22)


# noinspection PyPep8Naming
def Pump():
    return gpiozero.LED(27)


async def test():
    barrel = Barrel()
    pressure = Pressure()
    pump = Pump()
    pump.on()
    pointer = Pointer()
    for i in range(1000):
        air = pressure.get_pressure()
        if air is not None and air < 100000:
            barrel.servo.set_pos(40)
            pointer.on()
        else:
            barrel.servo.set_pos(-10)
            pointer.off()
        await asyncio.sleep(0.05)
