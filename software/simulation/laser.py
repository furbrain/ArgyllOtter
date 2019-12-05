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
    def __init__(self, timeout = 3.0):
        self.timeout = timeout
        
    def __del__(self):
        pass

    def __str__(self):
        return "Laser instance"

    @logged
    def on(self):
        pass

    @logged        
    def off(self):
        pass

    @logged        
    async def get_distance(self, speed=FAST):
        """Get laser range distance in mm"""
        return 1000

