#!/usr/bin/env python3
from . import mode, messages
import hardware
import asyncio
import time

ESCAPE_DATA = "/home/pi/escape_data.txt"
LEARN_SPEED = 400
LEARN_SPIN_SPEED = 200
CLEARANCE = 150
ORDER = "rRlLr"

class Handling:
    def __init__(self, speed, turn_speed, time_factor):
        self.speed = speed
        self.turn_speed = turn_speed
        self.laser_time_factor = time_factor
        
walking = Handling(400, 400, 0.53)
running = Handling(800, 800)

class Learn(mode.Mode):
    def on_start(self):
        self.data = open(ESCAPE_DATA, "w")
        self.laser = hardware.Laser()
        
    def handle_event(self, event):
        """Autonomous; no events handled"""
        return False
        
    async def run(self):
        for i in ORDER:
            if i in "rR":
                distance = await self.laser.get_distance()
                self.data.write("%d\n" % distance)
                await self.drive.a_goto(LEARN_SPEED, distance-CLEARANCE)
                await self.drive.spin(90, LEARN_SPIN_SPEED)
            elif i in "lL":
                distance = await self.laser.get_distance()
                self.data.write("%d\n" % distance)
                await self.drive.a_goto(LEARN_SPEED, distance-CLEARANCE)
                await self.drive.spin(-90, LEARN_SPIN_SPEED)
        #exit the course...
        await self.drive.a_goto(LEARN_SPEED, 1000)
        self.drive.stop()
        
class Walk(mode.Mode):
    def on_start(self):
        self.handling = walking
        self.laser = hardware.Laser()
        
    def get_distance(self):
        """return the distance of the wall in front and current position
        using the current offseet in the driver"""
        x1 = np.mean(self.drive.get_positions())
        y = await self.laser.get_distance()
        x2 = np.mean(self.drive.get_positions())
        distance = y + x1 + (x2-x1)*0.55
        return (distance, x2)
        
    def handle_event(self, event):
        """Autonomous; no events handled"""
        return False

    async def run(self):
        running = False
        self.drive.drive(self.handling.speed)
        for i in ORDER:
            wall, cur_pos = self.get_distance()
            if (wall - cur_pos) < 300:
                #shit we're too close.
                #stop and spin and try again...
                self.drive.stop()
                await asyncio.sleep(0.5)
                if i in "rR":
                    await self.drive.spin(90, LEARN_SPIN_SPEED)
                else:
                    await self.drive.spin(90, LEARN_SPIN_SPEED)
            if i in "RL":
                turn_start = 589 #values taken from piwars website
            else:
                turn_start = 793
                 
            if cur_pos < wall-turn_start:
                await self.drive.a_goto(self.handling.speed, wall-turn_start, 
                                        fast=True, reset_position=False, soft_start=True)
            #store power to enable smooth pull-out of turn...
            powers = self.drive.get_powers()
            #make the turn
            if i in "rR":
                await self.drive.fast_turn(90, self.handling.turn_speed)
            elif i in "lL":
                await self.drive.fast_turn(90, self.handling.turn_speed)
            #and pull out...
            self.drive.set_powers(*powers, reset_position=True)
        #exit the place
        await self.drive.a_goto(self.handling.speed, 1000, soft_start=True)
        # do a little dance
        await self.drive.spin(-10, 800)
        #make a little love
        await self.drive.spin(20, 800)
        # get down tonight
        await self.drive.spin(-10, 800)
        
class Run(Walk):
    def on_start(self):
        super().on_start()
        self.handling = running
