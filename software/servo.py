#!/usr/bin/env python3

class Servo:
    def __init__(self, pin="P1-7"):
        self.pin  = pinMode
        
    def set_pos(self, x):
        """Set position to x where -100 < x < 100
           Note this may not correspond to the actual degree position..."""
        with open("/dev/servoblaster","w") as f:
            val = 150 + x
            f.write(str(self.pin) + "=%f\n" % val)
            f.flush()
        
