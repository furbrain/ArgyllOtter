import asyncio

from util import start_task
from . import messages


class HardwareNotFoundError(Exception):
    pass


class Mode:
    HARDWARE = ("drive",)

    def __init__(self, joystick, hardware):
        self.joystick = joystick
        for item in self.HARDWARE:
            if getattr(hardware, item) is None:
                raise HardwareNotFoundError(item)
            setattr(self, item, getattr(hardware, item))

        self.on_start()
        self.task = start_task(self.run())

    def on_start(self):
        """this contains anything else that needs to be initialised"""
        pass

    def draw(self, screen):
        """this draws to the top_down arena in simulation"""
        pass

    def cancel(self):
        self.task.cancel()

    def handle_event(self, event):
        # returns true if event handled, otherwise returns false
        if isinstance(event, messages.ControllerConnectedMessage):
            self.joystick = event.joystick
            return True
        return False

    async def run(self):
        pass


class Interactive(Mode):
    def __init__(self, joystick, hardware):
        self.button_pressed = False
        super().__init__(joystick, hardware)

    def handle_event(self, event):
        if super().handle_event(event):
            return True
        if isinstance(event, messages.EncoderPressMessage):
            self.button_pressed = True
            return True
        if isinstance(event, messages.EncoderChangeMessage):
            self.change_event(event.pos)
            return True
        return False

    def change_event(self, up):
        pass

    async def wait_for_button(self):
        while True:
            if self.button_pressed:
                break
            await asyncio.sleep(0.2)
        self.button_pressed = False


class Null(Mode):
    HARDWARE = ('drive', 'camera')

    async def run(self):
        while True:
            await asyncio.sleep(1)
