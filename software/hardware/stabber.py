import time

import hardware.servo
import settings


class StabberPosition(settings.Settings):

    def default(self):
        self.stab = 400
        self.release = 0


class Stabber:
    def __init__(self):
        self.servo = hardware.servo.Servo(pin="1")
        self.positions = StabberPosition()

    def __enter__(self):
        self.stab()
        time.sleep(0.1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def stab(self):
        self.servo.set_pos(self.positions.stab)

    def release(self):
        self.servo.set_pos(self.positions.release)
