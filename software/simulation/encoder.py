#!/usr/bin/env python3

import time


class Encoder:
    # noinspection PyUnusedLocal
    def __init__(self, event_queue, pins=None):
        self.event_queue = event_queue
        self.last_press = time.time()

