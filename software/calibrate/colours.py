import cv2
import numpy as np
import PIL
import asyncio

from compute import vision
from modes import mode
from . import settings
import util

MIN_HUE = 1
MAX_HUE = 2
MIN_SAT = 3
MIN_VAL = 4

class Colours(settings.Settings):
    def default(self):
        self.red = ([-10,80,30],[10,255,255])
        self.yellow = ([25,120,30],[35,255,255])
        self.green = ([50,80,30],[70,255,255])
        self.blue = ([110,50,30],[130,255,255])

    def get_colour(self, text):
        return getattr(self, text)
        

class CalColour(mode.Interactive):
    HARDWARE = ["camera", "display"]
    def on_start(self):
        super().on_start()
        self.colour = Colours()
        self.current_col = [-10,80,30],[10,255,255]
        self.limits = {MIN_HUE: (-40,180),
                       MAX_HUE: (-40,180),
                       MIN_SAT: (0,255),
                       MIN_VAL: (0,255)} 
        self.mode = MIN_HUE
        self.image_shower = util.start_task(self.show_image())        
        
    def get_val_location(self):
        if self.mode == MIN_HUE:
            return 0,0
        elif self.mode == MAX_HUE:
            return 1,0
        elif self.mode == MIN_SAT:
            return 0,1
        elif self.mode == MIN_VAL:
            return 0,2
        
    def get_mode_text(self):
        if self.mode == MIN_HUE:
            return "hue"
        elif self.mode == MAX_HUE:
            return "HUE"
        elif self.mode == MIN_SAT:
            return "sat"
        elif self.mode == MIN_VAL:
            return "val"
        
    def change_event(self, up):
        x,y = self.get_val_location()
        if up:
            print("incrementing",x,y,self.current_col[x][y])
            self.current_col[x][y] += 4
        else:
            print("decrementing",x,y,self.current_col[x][y])
            self.current_col[x][y] -= 4
        
    def show_status(self, canvas):
        mode = self.get_mode_text()
        x,y = self.get_val_location()
        value = str(self.current_col[x][y])
        self.display.draw_text_on_canvas(mode, canvas, x=4, y=0, big=False)
        self.display.draw_text_on_canvas(value, canvas, x=98, y=0, big=False)
        
    async def show_image(self):
        while True:
            image = self.camera.get_image()
            mask = await util.spawn(vision.find_colour, image, self.current_col, False)
            mask = cv2.resize(mask, (128,64))
            mask = cv2.flip(mask, 1)
            with self.display.canvas() as draw:
                bitmap = PIL.Image.fromarray(mask)
                draw.bitmap((0, 0), bitmap, fill=1)
                self.show_status(draw)
            await asyncio.sleep(0.01)
        
    async def calibrate_colour(self, colour_name):
        print("aa")
        self.current_col = getattr(self.colour, colour_name)
        print("ab")
        self.mode = MIN_HUE
        await self.wait_for_button()
        print("bb")
        self.mode = MAX_HUE
        await self.wait_for_button()
        self.mode = MIN_SAT
        await self.wait_for_button()
        self.mode = MIN_VAL
        await self.wait_for_button()
        setattr(self.colour, colour_name, self.current_col)
        self.colour.save()
        
        
class CalibrateRed(CalColour):
    async def run(self):
        self.display.draw_text("Red")
        await self.calibrate_colour("red")
        self.display.clear()

class CalibrateAllColours(CalColour):
    async def run(self):
        for col in ("Red", "Green", "Yellow", "Blue"):
            self.display.draw_text(col)
            await self.calibrate_colour(col.lower())
        self.display.clear()

