#!/usr/bin/env python3
import sys

from hardware import Drive

d = Drive()
distance = int(sys.argv[1])
d.goto(400, distance)
