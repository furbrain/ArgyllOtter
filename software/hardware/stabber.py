import calibrate
import hardware.servo

class StabberPosition(calibrate.Settings):

    def default(self):
        self.stab = 400
        self.release = 0


class Stabber:
    def __init__(self):
        self.servo = hardware.servo.Servo(pin="0")
        self.positions = StabberPosition()

    def stab(self):
        self.servo.set_pos(self.positions.stab)

    def release(self):
        self.servo.set_pos(self.positions.release)