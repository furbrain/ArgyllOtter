#!/usr/bin/env python3
from .servo import Servo
import logging
from util import logged
import numpy as np
CAL_FILE = "/home/pi/grabber.npz"
class Grabber:
    def __init__(self):
        self.servo = Servo()
        try:
            d = np.load(CAL_FILE)
            self.opened = d['opened']
            self.closed = d['closed']
        except IOError:
            self.opened = 300
            self.closed = -500
            self.release = -100
            
    @logged    
    def open(self):
        self.servo.set_pos(self.opened)
        
    @logged
    def release(self):
        self.servo.set_pos(self.release)
    
    @logged    
    def close(self):
        self.servo.set_pos(self.closed)
        
    @logged
    def off(self):
        self.servo.off()
        
    def set_positions(self, opened, closed):
        self.opened = opened
        self.closed = closed
        np.savez(CAL_FILE, opened=opened, closed=closed)
