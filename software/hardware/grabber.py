#!/usr/bin/env python3
from .servo import Servo
import logging
from util import logged

class Grabber:
    def __init__(self):
        self.servo = Servo()
    
    @logged    
    def open(self):
        self.servo.set_pos(300)
    
    @logged    
    def close(self):
        self.servo.set_pos(-500)
