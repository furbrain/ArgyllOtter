#!/usr/bin/env python3
import asyncio
import logging
import math
import struct
import time

# noinspection PyUnresolvedReferences
import gpiozero
import numpy as np
# noinspection PyUnresolvedReferences
import smbus

import settings
from util import logged
from . import orientation

I2C_ADDRESS = 0x33
ALERT_REGISTER = 0x5F
RESET_POSITION = 0x01
SOFT_START = 0x02

DRIVE_CAL_FILE = "/home/pi/drivetrain.npz"


class DriveError(Exception):
    pass


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class DriveCalibration(settings.Settings):
    def default(self):
        self.spin_k = 0
        self.forward_k = 0
        self.reverse_k = 0


class Drive:
    def __init__(self, bus=None, wheel_diameter=70.0, clicks_per_revolution=374):
        if bus is None:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = bus
        self.cal = DriveCalibration()
        self.clicks_per_mm = clicks_per_revolution / (math.pi * wheel_diameter)
        self.orientation = orientation.Orientation(bus=self.bus)
        self.alert = gpiozero.Button(4)
        self.orientation.calibrate_gyro()
        self.stop(reset_position=True)

    def __str__(self):
        return "Drive instance"

    @staticmethod
    def get_flags(soft_start, reset_position):
        flags = 0
        if soft_start:
            flags |= SOFT_START
        if reset_position:
            flags |= RESET_POSITION
        return flags

    def reset_alert(self):
        self.get_alert()
        self.bus.write_i2c_block_data(I2C_ADDRESS, ALERT_REGISTER, [0])

    def get_alert(self):
        return self.bus.read_i2c_block_data(I2C_ADDRESS, ALERT_REGISTER, 1)[0]

    def mm2c(self, *args):
        return [int(x * self.clicks_per_mm) for x in args]

    def c2mm(self, *args):
        return [int(x / self.clicks_per_mm) for x in args]

    @logged
    def stop(self, reset_position=False):
        flags = self.get_flags(soft_start=False, reset_position=reset_position)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, [0, flags])

    @logged
    def drive(self, left, right=None, soft_start=False, reset_position=False):
        if right is None:
            right = left
        flags = self.get_flags(soft_start, reset_position)
        args = self.mm2c(left, right) + [soft_start]
        command = struct.pack("<BBhhB", 1, flags, *args)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))

    @logged
    def goto(self, max_speed, right, left=None, fast=False, soft_start=False, reset_position=True):
        flags = self.get_flags(soft_start, reset_position)
        if fast:
            cmd = 5
        else:
            cmd = 2
        if left is None:
            left = right
        args = self.mm2c(left, right, max_speed)
        # noinspection SpellCheckingInspection
        command = struct.pack("<BBiih", cmd, flags, *args)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))

    @logged
    def set_powers(self, fr, fl, rr, rl, soft_start=False, reset_position=False):
        args = fr, fl, rr, rl
        flags = self.get_flags(soft_start, reset_position)
        # noinspection SpellCheckingInspection
        command = struct.pack("<BBhhhh", 4, flags, *args)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))

    @logged
    def get_positions(self):
        for i in range(5):
            data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x10, 0x10)
            positions = struct.unpack("4i", bytes(data))
            if any(abs(x) > 10000 for x in positions):
                print("bad position, trying again")
                time.sleep(0.02)
                continue
            return self.c2mm(*positions)
        # noinspection PyUnboundLocalVariable
        raise DriveError(
            "Couldn't get reasonable positions, latest readings are" + ', '.join(str(x) for x in positions))

    @logged
    async def a_goto(self, max_speed, right, left=None, fast=False, soft_start=False, reset_position=True,
                     accurate=False):
        self.goto(max_speed, right, left, fast, soft_start, reset_position)
        while True:
            await asyncio.sleep(0.01)
            if not self.alert.is_pressed:
                await asyncio.sleep(0.01)
                if accurate:
                    await asyncio.sleep(0.1)
                return np.mean(self.get_positions())

    @logged
    def get_velocities(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x20, 0x08)
        velocities = struct.unpack("4h", bytes(data))
        return self.c2mm(*velocities)

    @logged
    def get_constants(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x30, 0x10)
        p, i, d, ratio = struct.unpack("4f", bytes(data))
        return {'kP': p, 'kI': i, 'kD': d, 'ratio': ratio}

    @logged
    def get_powers(self):
        powers = [0, 0, 0, 0]
        for i in range(5):
            data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x20, 0x10)
            powers = struct.unpack("<8h", bytes(data))[4:]
            if any(abs(x) > 1024 for x in powers):
                time.sleep(0.01)
                continue
            return powers
        raise DriveError("Couldn't get reasonable powers, latest readings are" + ', '.join(str(x) for x in powers))

    @logged
    def get_currents(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x40, 0x08)
        currents = struct.unpack("4h", bytes(data))
        return [x / 1000 for x in currents]

    @logged
    def get_voltages(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x50, 0x08)
        peripheral, _, main, _ = struct.unpack("4h", bytes(data))
        peripheral /= 1000.0
        main /= 1000.0
        return peripheral, main

    @logged
    async def spin(self, angle, max_speed, soft_start=False, reset_position=True, accurate=False):
        slow_speed = min(abs(max_speed), 300)
        slowed = False
        self.orientation.start_rotation()
        if angle > 0:
            left = max_speed
            slow_left = slow_speed
        else:
            left = -max_speed
            slow_left = -slow_speed
        right = -left
        slow_right = -slow_left
        k = self.cal.spin_k
        self.drive(left, right, soft_start=soft_start, reset_position=reset_position)
        while True:
            await asyncio.sleep(0.01)
            current_angle, v = self.orientation.get_total_rotation()
            if not slowed:
                if abs(current_angle - angle) < 30:
                    logging.debug("Spin: Current angle %f: slowed" % current_angle)
                    self.drive(slow_left, slow_right, soft_start=False, reset_position=False)
                    slowed = True
            if abs(current_angle) > (abs(angle) - k * v * v):  # kvv correction helps us stop on target
                logging.debug("Spin: Current angle %f: stopped" % current_angle)
                break
        self.stop()  # this sometimes is not received, so repeat after a short interval
        await asyncio.sleep(0.01)
        self.stop()
        if accurate:
            for i in range(20):
                await asyncio.sleep(0.01)
                current_angle, _ = self.orientation.get_total_rotation()
        return current_angle

    @logged
    async def fast_turn(self, angle, max_speed, differential=0.333, soft_start=False, reset_position=True):
        self.orientation.start_rotation()
        if angle > 0:
            self.drive(max_speed, max_speed * differential, soft_start=soft_start, reset_position=reset_position)
        else:
            self.drive(max_speed * differential, max_speed, soft_start=soft_start, reset_position=reset_position)
        while True:
            await asyncio.sleep(0.007)
            current_angle = self.orientation.get_total_rotation()
            if abs(current_angle) > abs(angle):
                logging.info("Fast_turn: Current angle %f: finished" % current_angle)
                break

    async def dance(self):
        # do a little dance
        self.drive(-800, 800)
        await asyncio.sleep(0.3)
        self.stop()
        await asyncio.sleep(0.1)
        # make a little love
        self.drive(800, -800)
        await asyncio.sleep(0.4)
        self.stop()
        await asyncio.sleep(0.1)
        # get down tonight
        self.drive(-800, 800)
        await asyncio.sleep(0.3)
        self.stop()

    async def finish(self):
        self.stop()


if __name__ == "__main__":
    async def go():
        d = Drive()
        await d.a_goto(400, 500, reset_position=True)
        await d.a_goto(400, 0, reset_position=False)  # should go back here
        await d.a_goto(400, 500, reset_position=True)
        await d.a_goto(400, 500, reset_position=True)  # should move forward here
        await d.a_goto(400, -1000, reset_position=True)  # and go back 1m (to starting position)
        await d.spin(360, 200)  # spin 360 degrees
        # now do some fast functions...
        await d.a_goto(400, 500, fast=True)
        powers = d.get_powers()
        print(powers)
        print("Positions: ", d.get_positions())
        print("Currents: ", d.get_currents())
        print("Velocities: ", d.get_velocities())
        print("Powers: ", d.get_powers())
        await d.fast_turn(90, 400)
        d.set_powers(*powers, reset_position=True)
        await asyncio.sleep(0.2)
        await d.a_goto(400, 800, soft_start=True, reset_position=False)
        await asyncio.sleep(1)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())
