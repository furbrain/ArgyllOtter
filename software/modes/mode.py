from . import messages

class Mode:
    def __init__(self, joystick):
        self.joystick = joystick
        
    def handle_event(self, event):
    #returns true if event handled, otherwise returns false
        if isinstance(event,messages.ControllerConnectedMessage):
            self.joystick = event.joystick
            return True
        return False
        
    async def run(self):
        pass
