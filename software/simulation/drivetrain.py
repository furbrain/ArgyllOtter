#!/usr/bin/env python3
import asyncio
import logging

import numpy as np

from util import logged


class DriveError(Exception):
    pass


class Drive:
    def __init__(self, shetty):
        self.shetty = shetty

    def __str__(self):
        return "Drive instance"

    @logged
    def stop(self, reset_position=False):
        self.shetty.stop()

    @logged
    def set_powers(self, fr, fl, rr, rl, soft_start=False, reset_position=False):
        self.shetty.spin(0)
        self.shetty.move(fr)

    @logged
    def get_powers(self):
        return [self.shetty.speed] * 4

    @logged
    def get_positions(self):
        dist = self.shetty.distance_counter
        return [dist] * 4

    @logged
    def drive(self, left, right=None, soft_start=False, reset_position=True):
        if right is None:
            right = left
        spin_rate = self.get_spin_rate(left, right)
        if reset_position:
            self.shetty.reset_position()
        self.shetty.spin(spin_rate)
        self.shetty.move((left + right) / 2)

    @logged
    async def a_goto(self, max_speed, right, left=None, fast=False, soft_start=False, reset_position=True,
                     accurate=False):
        if left is not None:
            raise NotImplemented("Can't handle differential goto in simulation")
        if reset_position:
            self.shetty.reset_position()
        self.shetty.spin(0)
        if right < 0:
            max_speed = -max_speed
        self.shetty.move(max_speed)
        while True:
            await asyncio.sleep(0.1)
            if max_speed > 0:
                if self.shetty.distance_counter > right:
                    break
            else:
                if self.shetty.distance_counter < right:
                    break
            if not fast and abs(self.shetty.distance_counter - right) < 200:
                self.shetty.move(max_speed / 4)
        self.stop()
        if accurate:
            await asyncio.sleep(0.1)
        return self.shetty.distance_counter

    @logged
    def get_velocities(self):
        raise NotImplemented

    @logged
    def get_constants(self):
        raise NotImplemented

    @logged
    def get_currents(self):
        return (0, 0, 0, 0)

    @logged
    def get_voltages(self):
        return (5, 11.6)

    def get_spin_rate(self, left, right):
        width = 200  # mm
        rate = 90 * (left - right) / (width * 2 * np.pi)
        return rate

    @logged
    async def spin(self, angle, max_speed, soft_start=False, reset_position=True, accurate=False):
        self.shetty.stop()

        slow_speed = min(abs(max_speed), 300)
        slowed = False

        if angle > 0:
            left = max_speed
            slow_left = slow_speed
        else:
            left = -max_speed
            slow_left = -slow_speed
        if False:  # FIXME was "if accurate:" - may want to leave as is currently
            right = 0
            slow_right = 0
        else:
            right = -left
            slow_right = -slow_left

        current_angle = 0
        start_angle = self.shetty.direction
        self.drive(left, right, soft_start=soft_start, reset_position=reset_position)
        while True:
            await asyncio.sleep(0.007)
            current_angle = self.shetty.direction - start_angle
            if not slowed:
                if abs(current_angle - angle) < 30:
                    logging.debug("Spin: Current angle %f: slowed" % current_angle)
                    self.drive(slow_left, slow_right, soft_start=False, reset_position=False)
                    slowed = True
            if abs(current_angle) > abs(angle):
                logging.debug("Spin: Current angle %f: stopped" % current_angle)
                break
        self.stop()  # this sometimes is not received, so repeat after a short interval
        if accurate:
            await asyncio.sleep(0.14)
            current_angle = self.shetty.direction - start_angle
        current_angle = -current_angle
        return current_angle

    @logged
    async def fast_turn(self, angle, max_speed, differential=0.333, soft_start=False, reset_position=True):
        current_angle = 0
        start_angle = self.shetty.direction
        rate = self.get_spin_rate(max_speed, max_speed * differential)
        self.shetty.move(max_speed * (differential + 1) / 2)
        if angle > 0:
            self.shetty.spin(rate)
        else:
            self.shetty.spin(-rate)
        while True:
            await asyncio.sleep(0.007)
            current_angle = self.shetty.direction - start_angle
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
