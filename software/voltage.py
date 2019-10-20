#!/usr/bin/env python3

from hardware import Drive
d = Drive()
print("V: ", d.get_voltages())
print("I: ", d.get_currents())

