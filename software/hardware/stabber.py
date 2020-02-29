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
        self.active = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.release()

    def stab(self):
        self.servo.set_pos(self.positions.stab)
        self.active = True
        return self

    def release(self):
        self.servo.set_pos(self.positions.release)
        self.active = False
        time.sleep(0.1)
        return self
