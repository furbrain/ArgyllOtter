#!/usr/bin/env python3

from gpiozero import Button
import logging
import time
from util import logged
from modes import messages

class Encoder():
    def __init__(self, event_queue, pins=None):
        if pins is None:
            pins = (26, 6, 19)
        self.event_queue = event_queue
        self.clock = Button(pins[0])
        self.data = Button(pins[1])
        self.switch = Button(pins[2])
        self.clock.when_pressed = self.movement
        self.switch.when_pressed = self.pressed    
        self.last_press = time.time()

    def add_event(self, msg):
        self.event_queue.put(msg)

    @logged
    def movement(self):
        if self.data.is_pressed:
            self.add_event(messages.EncoderChangeMessage(True))
        else:
            self.add_event(messages.EncoderChangeMessage(False))

    @logged
    def pressed(self):
        now = time.time()
        if now > (self.last_press+0.5):
            self.add_event(messages.EncoderPressMessage())
            self.last_press = now
        

if __name__=="__main__":
    # noinspection PyTypeChecker
    enc = Encoder(print, lambda: print("Button"))
    input("press Enter to finish")
