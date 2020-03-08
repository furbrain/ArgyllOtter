import asyncio

import numpy as np

from modes import mode


class Shooter(mode.Mode):
    HARDWARE = ['shooter']

    async def run(self):
        barrel = self.shooter.barrel
        rng = np.arange(*barrel.cal.range)
        up = []
        down = []
        for i in rng:
            barrel.servo.set_pos(i)
            await asyncio.sleep(1)
            up.append(barrel.orientation.get_angle())
        for i in reversed(rng):
            barrel.servo.set_pos(i)
            await asyncio.sleep(1)
            down.append(barrel.orientation.get_angle())
        barrel.cal.up = up
        barrel.cal.down = down[::-1]
        barrel.cal.save()
