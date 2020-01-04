#!/usr/bin/env python3
from modes import mode, messages
import asyncio
import time

class Grabber(mode.Interactive):
    HARDWARE = ('grabber', 'display')

    def on_start(self):
        super().on_start()
        self.grabber = hardware.Grabber()
        self.angle = 0
        self.display = hardware.Display()

    def handle_event(self, event):
        if super().handle_event(event):
            return True
        if isinstance(event, messages.EncoderChangeMessage):
            if event.pos:
                self.angle +=30
            else:
                self.angle -=30
            self.grabber.servo.set_pos(self.angle)
            return True
        return False
        
    async def run(self):
        self.display.draw_text("Open")
        await self.wait_for_button()
        opened = self.angle
        self.display.draw_text("Closed")
        await self.wait_for_button()
        closed = self.angle
        self.grabber.set_positions(opened, closed)
        self.display.clear()
        self.grabber.open()
        await asyncio.sleep(2)
        self.display.draw_text("NOM!")
        self.grabber.close()
        await asyncio.sleep(0.5)
        self.grabber.open()
        await asyncio.sleep(0.5)
        self.grabber.off()
