#!/usr/bin/env python3
import asyncio

from modes import mode


class Grabber(mode.Interactive):
    HARDWARE = ('grabber', 'display')

    def on_start(self):
        super().on_start()
        self.angle = 0

    def change_event(self, up):
        if up:
            self.angle += 30
        else:
            self.angle -= 30
        self.grabber.servo.set_pos(self.angle)

    def down_event(self):
        self.angle -= 30
        self.grabber.servo.set_pos(self.angle)

    async def run(self):
        cal = self.grabber.positions
        self.display.draw_text("Open")
        await self.wait_for_button()
        cal.opened = self.angle
        self.display.draw_text("Closed")
        await self.wait_for_button()
        cal.closed = self.angle
        self.display.draw_text("Release")
        await self.wait_for_button()
        cal.released = self.angle
        cal.save()
        self.display.clear()
        self.grabber.open()
        await asyncio.sleep(2)
        self.display.draw_text("NOM!")
        self.grabber.close()
        await asyncio.sleep(0.5)
        self.grabber.open()
        await asyncio.sleep(0.5)
        self.grabber.off()
