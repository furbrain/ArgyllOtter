#!/usr/bin/env python3

import asyncio
import collections
import os
import traceback

import calibrate
import menu
from modes import messages, shooter, escape, eco, manual, mode, lava
from util import start_task


class DiscardingQueue(collections.deque):
    def __init__(self, maxlen):
        super().__init__(maxlen=maxlen)

    def put(self, item):
        self.append(item)

    def get(self):
        return self.popleft()


class Main:
    def __init__(self, hardware=None):
        if hardware is None:
            import hardware
        self.events = DiscardingQueue(20)
        self.hardware = hardware.Hardware(self.events)
        self.mode = None
        self.finished = False
        self.joystick = None
        self.menu_items = [
            ("Manual", manual.Manual),
            ("Challenges", [
                ("Shooter", shooter.Shooter),
                ("Escape", [
                    ("Learn", escape.Learn),
                    ("Walk", escape.Walk),
                    ("Run", escape.Run)
                ]),
                ("Lava", [
                    ("Palava", lava.Lava),
                ]),
                ("Minesweeper", None),
                ("Eco-disaster", [
                    ("Test", eco.Test),
                    ("Main", eco.EcoDisaster),
                ]),
            ]),
            ("Calibrate", [
                ("Lens", calibrate.Lens),
                ("White Balance", calibrate.WhiteBalance),
                ("Camera Pos", calibrate.CameraPosition),
                ("Turning", calibrate.Spin),
                ("Grabber", calibrate.Grabber),
                ("Stabber", calibrate.StabberCal)
            ]),
            ("STOP", self.hardware.drive.stop),
            ("Debug", [
                ("Debug?", self.exit),
            ]),
            ("Shutdown", [
                ("Confirm", self.shutdown),
            ]),
        ]
        self.menu = menu.Menu(self.menu_items,
                              self.hardware,
                              self.handle_menu_select_item)

    def clear_displays(self):
        if self.hardware.display:
            self.hardware.display.clear()
        if self.hardware.pixels:
            self.hardware.pixels.clear()

    async def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.poll_events())
        while not self.finished:
            await asyncio.sleep(0.1)

    # noinspection PyBroadException
    async def enter_mode(self, modus):
        if self.mode:
            self.mode.cancel()
        self.clear_displays()
        if self.hardware.display:
            self.hardware.display.draw_text(modus.__name__)
        try:
            self.mode = modus(self.joystick, self.hardware)
            await self.mode.task
        except asyncio.CancelledError:
            pass
        except Exception:
            print("%s raised exception!" % modus.__name__)
            traceback.print_exc()
        finally:
            await self.mode.finish()
        self.mode = None
        self.menu.draw()

    def handle_menu_select_item(self, item):
        if item is None:
            return
        if isinstance(item, type) and issubclass(item, mode.Mode):
            start_task(self.enter_mode(item))
        else:
            item()

    def exit_mode(self):
        self.hardware.drive.stop()
        if self.mode:
            self.mode.cancel()
            self.mode = None

    @staticmethod
    def event_is_exit(event):
        if isinstance(event, messages.ControllerButtonMessage) and event.button == "home":
            return True
        # if isinstance(event, messages.EncoderPressMessage):
        #    return True
        return False

    def handle_event(self, event):
        if isinstance(event, messages.ControllerConnectedMessage):
            self.joystick = event.joystick
            return False  # continue processing this event...
        if self.mode is not None:
            if self.event_is_exit(event):
                self.exit_mode()
                return True
        return False

    async def poll_events(self):
        while True:
            if len(self.events):
                event = self.events.get()
                if self.handle_event(event):
                    pass
                elif self.mode is None:
                    self.menu.handle_event(event)
                else:
                    self.mode.handle_event(event)
            await asyncio.sleep(0.01)

    def draw(self, arena):
        if self.mode:
            self.mode.draw(arena)

    # noinspection PyMethodMayBeStatic
    def get_shape(self):
        return None

    def exit(self):
        self.clear_displays()
        self.finished = True

    def shutdown(self):
        self.clear_displays()
        self.finished = True
        os.system("sudo shutdown -h now")


# get up and running...
if __name__ == "__main__":
    m = Main()
    lp = asyncio.get_event_loop()
    lp.run_until_complete(m.run())
