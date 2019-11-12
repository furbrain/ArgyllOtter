#!/usr/bin/env python3
from . import mode, messages
import hardware
import asyncio
import time

ESCAPE_DATA = "/home/pi/escape_data.txt"
LEARN_SPEED = 400
LEARN_SPIN_SPEED = 200
CLEARANCE = 100
ORDER = "rrllrE"

class Handling:
    def __init__(self, speed, turn_speed, x_radius, y_radius):
        self.speed = speed
        self.turn_speed = turn_speed
        self.x_radius = x_radius
        self.y_radius = y_radius
        
walking = Handling(400, 400, 320, 320)

class Learn(mode.Mode):
    def on_start(self):
        self.data = open(ESCAPE_DATA, "w")
        self.laser = hardware.Laser()
        
    def handle_event(self, event):
        """Autonomous; no events handled"""
        return False
        
    async def run(self):
        for i in ORDER:
            if i == "r":
                distance = await self.laser.get_distance()
                self.data.write("%d\n" % distance)
                await self.drive.a_goto(LEARN_SPEED, distance-CLEARANCE)
                await self.drive.spin(90, LEARN_SPIN_SPEED)
            elif i == "l":
                self.data.write("%d\n" % distance)
                distance = await self.laser.get_distance()
                await self.drive.a_goto(LEARN_SPEED, distance-CLEARANCE)
                await self.drive.spin(-90, LEARN_SPIN_SPEED)
            elif i == "E":
                await self.drive.a_goto(LEARN_SPEED, 1000)
        self.drive.stop()
        
class Walk(mode.Mode):
    def on_start(self):
        with open(ESCAPE_DATA, "r") as f:
            self.distances = [int(x) for x in f]
        self.handling = walking
        
    def handle_event(self, event):
        """Autonomous; no events handled"""
        return False

    async def run(self):
        offset = 0
        for distance,direction in zip(self.distances, ORDER):
            print(distance, direction)
            if direction == "r":
                await self.drive.fast_goto(self.handling.speed, distance-CLEARANCE-self.handling.y_radius-offset)
                offset = self.handling.x_radius
                await self.drive.fast_spin(90, self.handling.turn_speed)
            elif direction == "l":
                await self.drive.fast_goto(self.handling.speed, distance-CLEARANCE-self.handling.y_radius-offset)
                offset = self.handling.x_radius
                await self.drive.spin(-90, self.handling.turn_speed)
            elif direction == "E":
                await self.drive.a_goto(self.handling.turn_speed, 1000)
        self.drive.stop()

