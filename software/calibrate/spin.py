import asyncio

import hardware
import modes


class Spin(modes.Interactive):
    HARDWARE = ['drive', 'stabber']
    async def run(self):
        await self.drive.spin(360,600)
        self.drive.stop()
        self.stabber.stab()
        await asyncio.sleep(1)
        await self.drive.spin(360,600)
        self.drive.stop()
        self.stabber.release()
