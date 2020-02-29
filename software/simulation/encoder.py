#!/usr/bin/env python3

import time

from modes import messages
from util import logged


class Encoder():
    def __init__(self, event_queue, pins=None):
        self.event_queue = event_queue
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
        if now > (self.last_press + 0.5):
            self.add_event(messages.EncoderPressMessage())
            self.last_press = now
