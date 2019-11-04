#!/usr/bin/env python3
from . import mode
from . import messages

import hardware
class Manual(mode.Mode):
    def __init__(self, joystick, normal=200, boost=1000):
        super().__init__(joystick)
        self.normal_speed = normal
        self.boost_speed = boost
        self.driver = hardware.Drive()
        
    def mixer(self, yaw, throttle, max_power):
        """
        Mix a pair of joystick axes, returning a pair of wheel speeds. This is where the mapping from
        joystick positions to wheel powers is defined, so any changes to how the robot drives should
        be made here, everything else is really just plumbing.
        
        :param yaw: 
            Yaw axis value, ranges from -1.0 to 1.0
        :param throttle: 
            Throttle axis value, ranges from -1.0 to 1.0
        :param max_power: 
            Maximum speed that should be returned from the mixer, defaults to 100
        :return: 
            A pair of power_left, power_right integer values to send to the motor driver
        """
        # make curves wider radius at high speed
        if max_power*throttle > 300:
            yaw = max(-0.5, yaw)
            yaw = min(0.5, yaw)
        
        # invert steering in reverse (more intuitive)
        if throttle < -0.1:
            yaw = -yaw
        left = throttle + yaw
        right = throttle - yaw
        scale = float(max_power) / max(1, abs(left), abs(right))
        return int(left * scale), int(right * scale)

    async def run(self):
        while True:
            if self.joystick and self.joystick.connected:
                x_axis, y_axis = self.joystick['lx', 'ly']
                if x_axis == y_axis == 0.0:
                    self.driver.stop()
                else:
                    boost = self.joystick['r1']
                    if boost:
                        max_power=self.boost_speed
                    else:
                        max_power=self.normal_speed
                    # Get power from mixer function
                    power_left, power_right = self.mixer(yaw=x_axis, throttle=y_axis, max_power=max_power)
                    # Set motor speeds
                    self.driver.drive(power_left, power_right)
            else:
                self.driver.stop()

