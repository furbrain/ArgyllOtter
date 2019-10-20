#!/usr/bin/env python3

class Servo:
    def __init__(self, pin="0", inverted=False):
        self.pin  = pin
        self.inverted = inverted
        
    def set_servo(self, val):
        with open("/dev/servoblaster","w") as f:
            f.write(str(self.pin) + "=%f\n" % val)
            f.flush()
        
    def set_pos(self, x):
        """Set position to x where -50 < x < 250
           Note this may not correspond to the actual degree position..."""
        if self.inverted:
            x = -x
        val = x - 150
        self.set_servo(val)
                
    def off(self):
        """Turn servo off"""
        self.set_servo(0)
    
