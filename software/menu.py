#!/usr/bin/env python3
from oled.device import sh1106, const
from oled.render import canvas
from PIL import ImageFont
import time

class Menu():
    """This class takes a nested array of pairs in key, value format
    where key is a text to show on a menu, and value is either a sub-menu
    or a single callback that takes no arguments"""
    
    def __init__(self, menu_array):
        self.menu_array = menu_array
        self.display = sh1106(port=1, address=0x3C) #create display
        self.display.command(const.COMSCANINC, const.SEGREMAP) #invert it
        self.font = ImageFont.truetype("DejaVuSans.ttf",16)
        self.index = 0

    def item_changed(self, pos):
        self.index = pos % (len(self.menu_array))
                
    def item_selected(self):
        print("Item %d selected" % self.index)
        
    def draw(self):
        with canvas(self.display) as c:
            c.rectangle(((0, self.index*16), (128, (self.index+1)*16)), fill=255)
            for i, (text, action) in enumerate(self.menu_array):
                fill = 0 if i==self.index else 255
                c.text((0,i*16), text, font=self.font, fill=fill)
        

if __name__ == "__main__":
    from drivetrain import DriveTrain
    from encoder import Encoder
    d = DriveTrain()
    test = [
        ("Move", [
            ("Forward 1m", lambda : d.goto(1000, 1000, 800)),
            ("Backward 1m", lambda: d.goto(0, 0, 800))]),
        ("Manual", d.stop),
        ("Challenge", None),
        ("Debug", None)]
    m = Menu(test)
    m.draw()
    e = Encoder((19,13,26), m.item_changed, m.item_selected)
    while True:
        time.sleep(0.1)
        m.draw()

