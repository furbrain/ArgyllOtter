#!/usr/bin/env python3
import asyncio
import time
import re
import logging
from util import logged

class LaserTimeoutError(Exception):
    pass
    
class LaserBadReadingError(Exception):
    pass

class Laser:
    FAST = b'F'
    MEDIUM = b'D'
    SLOW = b'M'
    def __init__(self, shetty, arena, timeout = 3.0):
        self.shetty = shetty
        self.arena = arena
        self.timeout = timeout
        
    def __del__(self):
        pass

    def __str__(self):
        return "Laser instance"

    @logged
    def on(self):
        self.shetty.laser = True

    @logged        
    def off(self):
        self.shetty.laser = False

    @logged        
    async def get_distance(self, speed=FAST):
        """Get laser range distance in mm"""
        await asyncio.sleep(0.4)
        distance = self.shetty.get_distance(self.arena)
        await asyncio.sleep(0.3)
        return distance
