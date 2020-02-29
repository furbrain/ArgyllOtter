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


class ControllerButtonMessage(ControllerMessage):
    def __init__(self, button):
        self.button = button


class ControllerConnectedMessage(ControllerMessage):
    def __init__(self, connected, joystick=None):
        self.connected = connected
        self.joystick = joystick
