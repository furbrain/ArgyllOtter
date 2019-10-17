#!/usr/bin/env python3

class Servo:
    def __init__(self, pin="0"):
        self.pin  = pin
        
    def set_pos(self, x):
        """Set position to x where 50 < x < 250
           Note this may not correspond to the actual degree position..."""
        with open("/dev/servoblaster","w") as f:
            f.write(str(self.pin) + "=%f\n" % x)
            f.flush()
        
    def off(self):
        """Turn servo off"""
        with open("/dev/servoblaster","w") as f:
            f.write(str(self.pin) + "=0\n")
            f.flush()
    
