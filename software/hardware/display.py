from oled.device import sh1106, const
from oled.render import canvas

class Display:
    def __init__(self):
        self.oled = sh1106(port=1, address=0x3C) #create display
        self.oled.command(const.COMSCANINC, const.SEGREMAP) #invert it

    def canvas(self):
        return canvas(self.oled)
