#!/usr/bin/env python3
import logging
from util import logged

class Servo:
    def __init__(self, pin="0", inverted=False):
        self.pin  = pin
        self.inverted = inverted
        
    def __del__(self):
        self.off()
        
    @logged
    def set_servo(self, val):
        with open("/dev/servoblaster","w") as f:
            f.write(str(self.pin) + "=%dus\n" % int(val))
            f.flush()
        
    @logged
    def set_pos(self, x):
        """Set position to x where -1000 < x < 1000
           Note this may not correspond to the actual degree position..."""
        if self.inverted:
            x = -x
        val = 1500 + x
        self.set_servo(val)
                
    @logged
    def off(self):
        """Turn servo off"""
        self.set_servo(0)
    
