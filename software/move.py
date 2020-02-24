#!/usr/bin/env python3
from hardware import Drive
import sys
d = Drive()
distance = int(sys.argv[1])
d.goto(400, distance)
