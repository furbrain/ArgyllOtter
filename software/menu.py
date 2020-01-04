#!/usr/bin/env python3
import time
import copy

from modes import messages

COLORS = ((0,0,80),
          (0,80,0),
          (60,60,0),
          (60,0,60))

class BackMenuItem():
    pass

class Menu():
    """This class takes a nested array of pairs in key, value format
    where key is a text to show on a menu, and value is either a sub-menu
    or a single callback that takes no arguments"""
    
    def __init__(self, menu_array, hardware, action_item, depth=0, parent = None):
        self.menu_array = menu_array
        self.hardware = hardware
        self.depth = depth
        self.index = 0
        self.child = None
        self.parent = parent
        self.action_item = action_item
        self.offset = 0
        if self.parent is not None:
            self.menu_array.append(("Back", BackMenuItem()))
        self.draw()
        
    def handle_event(self, event):
        if isinstance(event, messages.ControllerButtonMessage):
            if event.button == "dup":
                self.item_changed(False)
                return True
            elif event.button == "ddown":
                self.item_changed(True)
                return True
            elif event.button == "start":
                self.item_selected()
                return True
        elif isinstance(event, messages.EncoderChangeMessage):
            self.item_changed(event.pos)
            return True
        elif isinstance(event, messages.EncoderPressMessage):
            self.item_selected()
            return True
        return False        

    def item_changed(self, pos):
        if self.child is None:
            if pos:
                self.index += 1
            else:
                self.index -= 1
            self.index = self.index % (len(self.menu_array))
        else:
            self.child.item_changed(pos)
        self.draw()
                
    def item_selected(self):
        if self.child is None:
            text, item = self.menu_array[self.index]
            if isinstance(item, list):
                self.child = Menu(item, self.hardware, self.action_item, 
                                  depth = self.depth+1, parent=self)
            elif isinstance(item, BackMenuItem):
                self.parent.child_exit()
            else:
                if item is not None:
                    self.action_item(item)
        else:
            self.child.item_selected()
        
    def child_exit(self):
        self.child = None  
        self.draw()  
        
    def draw(self):
        if self.child is None:
            pixels = self.hardware.pixels
            for i in range(pixels.numPixels()):
                pixels.setPixelColorRGB(i,0,0,0)
            for i in range(self.index+1):
                pixels.setPixelColorRGB(i,*COLORS[self.depth])
            pixels.show()
            if self.hardware.display:
                with self.hardware.display.canvas() as c:
                    self.offset = min(self.index, self.offset)
                    self.offset = max(self.index-3, self.offset)
                    c.rectangle(((0, (self.index-self.offset)*16), (128, (self.index-self.offset+1)*16)), fill=255)
                    for i, (text, action) in enumerate(self.menu_array):
                        fill = 0 if i==self.index else 255
                        self.hardware.display.draw_text_on_canvas(text, c, x=None, y=(i-self.offset)*16, fill=fill, big=False)
        else:
            self.child.draw()        

