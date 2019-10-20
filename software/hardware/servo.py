#!/usr/bin/env python3

class Servo:
    def __init__(self, pin="0", inverted=False):
        self.pin  = pin
        self.inverted = inverted
        
    def __del__(self):
        self.off()
        
    def set_servo(self, val):
        with open("/dev/servoblaster","w") as f:
            f.write(str(self.pin) + "=%f\n" % val)
            f.flush()
        
    def set_pos(self, x):
        """Set position to x where -100 < x < 100
           Note this may not correspond to the actual degree position..."""
        if self.inverted:
            x = -x
        val = 150 + x
        self.set_servo(val)
                
    def off(self):
        """Turn servo off"""
        self.set_servo(0)
    
