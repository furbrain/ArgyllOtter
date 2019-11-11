#!/usr/bin/env python3
from . import mode, messages
import hardware
import asyncio
import time

ESCAPE_DATA = "/home/pi/escape_data.txt"
LEARN_SPEED = 400
CLEARANCE = 50
ORDER = "rrllrE"

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
                await self.spin(90)
            elif i == "l":
                self.data.write("%d\n" % distance)
                distance = await self.laser.get_distance()
                await self.drive.a_goto(LEARN_SPEED, distance-CLEARANCE)
                await self.spin(90)
            elif i == "E":
                await self.drive.a_goto(LEARN_SPEED, 1000)
        self.drive.stop()
