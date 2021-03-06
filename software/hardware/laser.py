#!/usr/bin/env python3
import asyncio
import logging
import re
import time

import serial

from util import logged

BAUD_RATE = 19200


class LaserTimeoutError(Exception):
    pass


class LaserBadReadingError(Exception):
    pass


class Laser:
    FAST = b'F'
    MEDIUM = b'D'
    SLOW = b'M'
    TimeoutError = LaserTimeoutError
    BadReadingError = LaserBadReadingError

    def __init__(self, timeout=3.0):
        self.timeout = timeout
        self.port = serial.Serial("/dev/serial0", 19200, timeout=0)  # yes *this* timeout should be zero

    def __del__(self):
        self.port.close()

    def __str__(self):
        return "Laser instance"

    @logged
    def on(self):
        self.port.write(b'O')

    @logged
    def off(self):
        self.port.write(b'C')

    @logged
    async def get_distance(self, speed=FAST):
        """Get laser range distance in mm"""
        self.port.reset_input_buffer()
        start_time = time.time()
        self.port.write(speed)
        buffer = b''
        while True:
            buffer += self.port.read(20)
            if b'\n' in buffer:
                break
            await asyncio.sleep(0.1)
            if time.time() > start_time + self.timeout:
                raise LaserTimeoutError()
        logging.info("Laser return is %s", str(buffer))
        dist = re.search(r"(\d*\.\d*)m", str(buffer))
        if dist is None:
            raise LaserBadReadingError()
        return int(float(dist.group(1)) * 1000)

    async def finish(self):
        self.off()


if __name__ == "__main__":
    async def run():
        laser = Laser()
        print(await laser.get_distance())


    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
