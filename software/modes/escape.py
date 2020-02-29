#!/usr/bin/env python3
import asyncio

import numpy as np

from . import mode

ESCAPE_DATA = "/home/pi/escape_data.txt"
LEARN_SPEED = 400
LEARN_SPIN_SPEED = 100
CLEARANCE = 250
ORDER = "rRlLr"


class Handling:
    def __init__(self, speed, turn_speed, time_factor, clearance):
        self.speed = speed
        self.turn_speed = turn_speed
        self.laser_time_factor = time_factor
        self.clearance = clearance


walking = Handling(400, 300, 0.53, 50)
running = Handling(600, 300, 0.62, 0.33)


class Learn(mode.Mode):
    HARDWARE = ('drive', 'laser')

    def on_start(self):
        self.data = open(ESCAPE_DATA, "w")

    def handle_event(self, event):
        """Autonomous; no events handled"""
        return False

    async def run(self):
        for i in ORDER:
            distance = await self.laser.get_distance()
            self.data.write("%d\n" % distance)
            await self.drive.a_goto(LEARN_SPEED, distance - CLEARANCE)
            await asyncio.sleep(0.2)
            if i in "rR":
                await self.drive.spin(88, LEARN_SPIN_SPEED)
            elif i in "lL":
                await self.drive.spin(-86, LEARN_SPIN_SPEED)
            await asyncio.sleep(0.2)
        # exit the course...
        self.data.close()
        await self.drive.a_goto(LEARN_SPEED, 1000)
        self.drive.stop()
        await self.drive.dance()


class Walk(mode.Mode):
    HARDWARE = ('drive', 'laser')

    def on_start(self):
        self.handling = walking

    async def get_distance(self):
        """return the distance of the wall in front and current position
        using the current offseet in the driver"""
        pos1 = self.drive.get_positions()
        x1 = np.mean(pos1)
        y = await self.laser.get_distance()
        pos2 = self.drive.get_positions()
        x2 = np.mean(pos2)
        distance = y + x1 + (x2 - x1) * 0.55
        print("get_distance: ", x1, x2, y, distance, pos1, pos2)
        return (distance, x2)

    def handle_event(self, event):
        """Autonomous; no events handled"""
        return False

    async def run(self):
        running = False
        self.drive.drive(self.handling.speed, reset_position=True)
        powers = None
        for i in ORDER:
            await asyncio.sleep(0.05)
            for _ in range(4):
                wall, cur_pos = await self.get_distance()
                if wall < 3000:
                    break
                self.drive.stop()
            # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable
            if (wall - cur_pos) < 400:
                # shit we're too close.
                # stop and spin and try again...
                print("AAAAAAAAGGGGHHHHH")
                self.drive.stop()
                await asyncio.sleep(0.5)
                if i in "rR":
                    await self.drive.spin(90, LEARN_SPIN_SPEED)
                else:
                    await self.drive.spin(-90, LEARN_SPIN_SPEED)
            else:
                if i in "RL":
                    turn_start = 500 + self.handling.clearance  # values taken from piwars website
                else:
                    turn_start = 700 + self.handling.clearance

                if cur_pos < wall - turn_start:
                    print(await self.drive.a_goto(self.handling.speed, wall - turn_start,
                                                  fast=True, reset_position=False, soft_start=True))
                # store power to enable smooth pull-out of turn...
                powers = self.drive.get_powers()
                # make the turn
                if i in "rR":
                    await self.drive.fast_turn(90, self.handling.turn_speed, differential=0)
                    # await self.drive.fast_turn(10, self.handling.turn_speed, differential=0.6)
                elif i in "lL":
                    await self.drive.fast_turn(-90, self.handling.turn_speed, differential=0)
                    # await self.drive.fast_turn(-10, self.handling.turn_speed, differential=0.8)
            # and pull out...
            if powers is not None:
                self.drive.set_powers(*powers, reset_position=True)
        # exit the place
        await self.drive.a_goto(self.handling.speed, 1000, soft_start=True)
        # do a little dance
        self.drive.stop()
        await asyncio.sleep(0.2)
        await self.drive.dance()


class Run(mode.Mode):
    HARDWARE = ('drive', 'laser')

    def on_start(self):
        super().on_start()
        self.handling = running
        with open(ESCAPE_DATA, "r") as f:
            self.distances = [int(x.strip()) for x in f]
        print(self.distances)
