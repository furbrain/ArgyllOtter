#!/usr/bin/env python3
from .servo import Servo
import logging
from util import logged
import numpy as np
import calibrate

class GrabPositions(calibrate.Settings):
    def default(self):
        self.opened = 300
        self.closed = -500
        self.released = -100
        
class Grabber:
    def __init__(self):
        self.servo = Servo()
        self.positions = GrabPositions()
            
    @logged    
    def open(self):
        self.servo.set_pos(self.positions.opened)
        
    @logged
    def release(self):
        self.servo.set_pos(self.positions.released)
    
    @logged    
    def close(self):
        self.servo.set_pos(self.positions.closed)
        
    @logged
    def off(self):
        self.servo.off()
