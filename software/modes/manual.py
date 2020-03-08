#!/usr/bin/env python3
import asyncio

from util import start_task
from . import messages
from . import mode


# noinspection PyAttributeOutsideInit
class Manual(mode.Mode):
    HARDWARE = ('drive',)

    def on_start(self):
        self.slow_speed = 40
        self.normal_speed = 200
        self.boost_speed = 1000
        self.speed = self.normal_speed
        self.turning = False

    async def turn(self, degrees):
        self.turning = True
        print("starting turn")
        await self.drive.spin(degrees, self.speed)
        print("turn finished")
        self.turning = False

    def handle_event(self, event):
        if super().handle_event(event):
            return True
        if isinstance(event, messages.ControllerButtonMessage):
            if event.button == "l2":
                start_task(self.turn(-90))
                return True
            elif event.button == "r2":
                start_task(self.turn(90))
                return True
        return False

    @staticmethod
    def mixer(yaw, throttle, max_power):
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
        if max_power * throttle > 300:
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
            await asyncio.sleep(0.1)

            if self.joystick and self.joystick.connected:
                x_axis, y_axis = self.joystick['lx', 'ly']
                if not self.turning:
                    if x_axis == y_axis == 0.0:
                        self.drive.stop()
                    else:
                        if self.joystick['r1']:
                            self.speed = self.boost_speed
                        elif self.joystick['l1']:
                            self.speed = self.slow_speed
                        else:
                            self.speed = self.normal_speed
                        # Get power from mixer function
                        power_left, power_right = self.mixer(yaw=x_axis, throttle=y_axis, max_power=self.speed)
                        # Set motor speeds
                        self.drive.drive(power_left, power_right)
            else:
                self.drive.stop()
