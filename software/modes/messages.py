class Message:
    def __str__(self):
        return self.__class__.__name__ + ": " + str(self.__dict__)
    
class EncoderMessage(Message):
    pass
    
class EncoderPressMessage(EncoderMessage):
    pass

class EncoderChangeMessage(EncoderMessage):
    def __init__(self, pos):
        self.pos = pos
        
class ControllerMessage(Message):
    pass
    
class ControllerAxisMessage(ControllerMessage):
    def __init__(self, side, x, y):
        self.side = side
        self.x = x
        self.y = y
        
class ControllerButtonMessage(ControllerMessage):
    def __init__(self, button):
        self.button = button
        
class ControllerConnectedMessage(ControllerMessage):
    def __init__(self, connected):
        self.connected = connected
