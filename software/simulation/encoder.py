#!/usr/bin/env python3

import time

from modes import messages
from util import logged


class Encoder:
    def __init__(self, event_queue, pins=None):
        self.event_queue = event_queue
        self.last_press = time.time()

