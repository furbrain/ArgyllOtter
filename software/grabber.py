#!/usr/bin/env python3
from servo import Servo

class Grabber:
    def __init__(self):
        self.servo = Servo()
        
    def open(self):
        self.servo.set_pos(30)
        
    def close(self):
        self.servo.set_pos(-50)
