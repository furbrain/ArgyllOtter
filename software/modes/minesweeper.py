import asyncio
import time
from functools import partial

from compute import vision
from . import mode

SPIN_SPEED = 400
TURN_SPEED = 200
DRIVE_SPEED = 600

FORWARD = 0
LEFT = 1
RIGHT = 2
STOP = 3


class Blob:
    def __init__(self, contour):
        self.min_x = min(contour[:, :, 0])[0]
        self.max_x = max(contour[:, :, 0])[0]
        self.centre_x = (self.min_x + self.max_x) / 2
        self.max_y = max(contour[:, :, 1])[0]

    def at_left(self):
        return self.min_x < 10

    def at_right(self):
        return self.max_x > 630

    def get_direction(self):
        if 220 < self.centre_x < 420:
            if self.max_y > 460:
                return STOP
            return FORWARD
        if self.centre_x < 260:
            return LEFT
        if self.centre_x > 380:
            return RIGHT


# noinspection PyAttributeOutsideInit
class MineSweeper(mode.Mode):
    HARDWARE = ('drive', 'camera', 'display')

    def on_start(self):
        self.actions = {
            STOP: None,
            LEFT: partial(self.drive.drive, 0, TURN_SPEED),
            RIGHT: partial(self.drive.drive, TURN_SPEED, 0),
            FORWARD: partial(self.drive.drive, DRIVE_SPEED)
        }

    def draw(self, arena):
        pass

    async def get_blob(self):
        image = await self.camera.a_get_image()
        ct = vision.find_biggest_contour(image, "red")
        if ct is None:
            return None
        return Blob(ct)

    async def hunt(self):
        while True:
            b = await self.get_blob()
            if b is not None:
                direction = b.get_direction()
                if direction == STOP:
                    await self.drive.a_goto(DRIVE_SPEED, 400, fast=True)
                    break
                elif direction == LEFT:
                    self.drive.drive(0, TURN_SPEED)
                elif direction == RIGHT:
                    self.drive.drive(TURN_SPEED, 0)
                elif direction == FORWARD:
                    self.drive.drive(DRIVE_SPEED)
            await asyncio.sleep(0.05)

    async def find_left(self):
        self.drive.drive(-TURN_SPEED, TURN_SPEED)
        while True:
            b = await self.get_blob()
            if b is not None:
                await self.hunt()
                return
            await asyncio.sleep(0.05)

    async def spin(self):
        self.drive.drive(SPIN_SPEED, -SPIN_SPEED)
        spin_start = time.time()
        while True:
            b = await self.get_blob()
            if b is not None:
                self.drive.stop()
                return
            if time.time() > spin_start + 2:
                self.drive.stop()
                # take a break in case we are already on the right square
                await asyncio.sleep(2)
                self.drive.drive(SPIN_SPEED, -SPIN_SPEED)
                spin_start = time.time()
            await asyncio.sleep(0.1)

    async def run(self):
        # look for red
        while True:
            await self.spin()
            await asyncio.sleep(0.3)
            b = await self.get_blob()
            if b is None:
                await self.find_left()
            else:
                await self.hunt()
            await asyncio.sleep(2)
