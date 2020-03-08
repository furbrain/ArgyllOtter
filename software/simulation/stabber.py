import asyncio

import settings


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class StabberPosition(settings.Settings):

    def default(self):
        self.stab = 400
        self.release = 0


class Stabber:
    def __init__(self):
        self.positions = StabberPosition()
        self.active = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.release()
        await asyncio.sleep(0.1)

    async def stab(self):
        self.active = True
        await asyncio.sleep(0.1)
        return self

    def release(self):
        self.active = False
        return self

    async def finish(self):
        pass
