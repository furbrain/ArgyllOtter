from . import messages
import asyncio

class Mode:
    def __init__(self, joystick, drive, pixels):
        self.joystick = joystick
        self.drive = drive
        self.pixels = pixels
        self.on_start()
        self.task = asyncio.ensure_future(self.run())
        
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
