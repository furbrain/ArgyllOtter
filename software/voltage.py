#!/usr/bin/env python3
from drivetrain import DriveTrain
import time

d = DriveTrain()
print("V: ", d.get_voltages())
print("I: ", d.get_currents())

