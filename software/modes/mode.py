from . import messages
import asyncio
from util import start_task

class HardwareNotFoundError(Exception):
    pass

class Mode:
    HARDWARE = ()
    
    def __init__(self, joystick, hardware):        
        self.joystick = joystick
        for item in self.HARDWARE:
            if getattr(hardware,item) is None:
                raise HardwareNotFoundError(item)
            setattr(self,item,getattr(hardware,item))
            
        self.on_start()
        self.task = start_task(self.run())
        
    def on_start(self):
        """this contains anything else that needs to be initialised"""
        pass
        
    def draw(self):
        """this draws to the top_down arena in simulation"""
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
    def __init__(self, joystick, hardware):
        self.button_pressed = False
        super().__init__(joystick, hardware)

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

