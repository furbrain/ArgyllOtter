from . import messages
import asyncio
from utils import start_task

class Mode:
    def __init__(self, joystick, drive, pixels):
        self.joystick = joystick
        self.drive = drive
        self.pixels = pixels
        self.on_start()
        self.task = start_task(self.run())
        
    def on_start(self):
        """this contains anything else that needs to be initialised"""
        pass
    
    def cancel(self):
        self.task.cancel()
        
    def handle_event(self, event):
    #returns true if event handled, otherwise returns false
        if isinstance(event,messages.ControllerConnectedMessage):
            self.joystick = event.joystick
            return True
        return False
        
    async def run(self):
        pass
        
class Interactive(Mode):
    def __init__(self, joystick, drive, pixels):
        self.button_pressed = False
        super().__init__(joystick, drive, pixels)

    def handle_event(self, event):
        if super().handle_event(event):
            return True
        if isinstance(event, messages.EncoderPressMessage):
            self.button_pressed = True
            return True
        return False
    
    async def wait_for_button(self):
        while True:
            if self.button_pressed:
                break
            await asyncio.sleep(0.1)
        self.button_pressed=False

