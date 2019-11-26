#!/usr/bin/env python3

from gpiozero import Button
import logging
import time
from util import logged


class Encoder():
    def __init__(self, on_changed, on_pressed, pins=None):
        if pins is None:
            pins = (26, 6, 19)
        self.on_changed = on_changed
        self.on_pressed = on_pressed
        self.clock = Button(pins[0])
        self.data = Button(pins[1])
        self.switch = Button(pins[2])
        self.clock.when_pressed = self.movement
        self.switch.when_pressed = self.pressed    
        self.last_press = time.time()

    @logged
    def movement(self):
        if self.data.is_pressed:
            self.on_changed(True)
        else:
            self.on_changed(False)

    @logged
    def pressed(self):
        now = time.time()
        if now > (self.last_press+0.5):
            self.on_pressed()
            self.last_press = now
        

if __name__=="__main__":
    enc = Encoder(print, lambda: print("Button"))
    input("press Enter to finish")
