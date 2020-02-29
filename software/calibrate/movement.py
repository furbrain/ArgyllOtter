#!/usr/bin/env python3
import asyncio
import time

import numpy as np

from modes import mode


class Spin(mode.Mode):
    HARDWARE = ('drive', 'display')

    def on_start(self):
        self.o = self.drive.orientation

    async def get_k(self):
        start = time.time()
        self.o.start_rotation()
        while True:
            await asyncio.sleep(0.02)
            rot, v = self.o.get_total_rotation()
            now = time.time() - start
            if now > 1.0:
                break
        self.drive.stop()
        while True:
            await asyncio.sleep(0.02)
            self.o.get_total_rotation()
            now = time.time() - start
            if now > 1.5:
                break
        self.drive.stop()
        final_rot, _ = self.o.get_total_rotation()
        print("v ", v)
        s = final_rot - rot
        k = s / (v * v)
        await asyncio.sleep(0.1)
        return abs(k)

    async def test(self, speed, accurate, rev=False):
        angle = np.random.randint(40, 180)
        if rev:
            angle = -angle
        true_angle = await self.drive.spin(angle, speed, accurate=accurate)
        offset = true_angle - angle
        print("Speed: %d, angle, %.4g error %.4g" % (speed, angle, offset))

    async def do_calibration(self):
        spin = []
        forward = []
        reverse = []
        for speed in [200, 250, 300, 350, 400]:
            self.drive.drive(speed, -speed)
            k = await self.get_k()
            if k < 0.001:
                spin.append(k)
            self.drive.drive(speed, 0)
            k = await self.get_k()
            if k < 0.001:
                forward.append(k)
            self.drive.drive(-speed, 0)
            k = await self.get_k()
            if k < 0.001:
                reverse.append(k)

        self.drive.cal.spin_k = np.mean(spin)
        self.drive.cal.forward_k = np.mean(forward)
        self.drive.cal.reverse_k = np.mean(reverse)
        print(self.drive.cal.__dict__)
        self.drive.cal.save()

    async def do_testing(self, accurate, rev=False):
        self.display.draw_text("Testing")
        for speed in [200, 300, 400, 500, 600]:
            await self.test(speed, accurate, rev)

    async def run(self):
        await self.do_calibration()
