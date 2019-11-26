#!/usr/bin/env python3
from PIL import ImageFont
import time
import copy

from hardware import Display

class BackMenuItem():
    pass

class Menu():
    """This class takes a nested array of pairs in key, value format
    where key is a text to show on a menu, and value is either a sub-menu
    or a single callback that takes no arguments"""
    
    def __init__(self, menu_array, action_item, display = None, parent = None):
        self.menu_array = menu_array
        if display is None:
            self.display = Display()
        else:
            self.display = display
        self.font = ImageFont.truetype("DejaVuSans.ttf",16)
        self.index = 0
        self.child = None
        self.parent = parent
        self.action_item = action_item
        self.offset = 0
        if self.parent is not None:
            self.menu_array.append(("Back", BackMenuItem()))
        self.draw()
        
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
                self.child = Menu(item, self.action_item, display=self.display, parent=self)
            elif isinstance(item, BackMenuItem):
                self.parent.child_exit()
            else:
                if item is not None:
                    self.action_item(item)
        else:
            self.child.item_selected()
        
    def child_exit(self):
        self.child = None    
        
    def draw(self):
        if self.child is None:
            with self.display.canvas() as c:
                self.offset = min(self.index, self.offset)
                self.offset = max(self.index-3, self.offset)
                c.rectangle(((0, (self.index-self.offset)*16), (128, (self.index-self.offset+1)*16)), fill=255)
                for i, (text, action) in enumerate(self.menu_array):
                    fill = 0 if i==self.index else 255
                    size = c.textsize(text, font=self.font)
                    h_offset = max(0, (128-size[0]) // 2)
                    c.text((h_offset,(i-self.offset)*16), text, font=self.font, fill=fill)
        else:
            self.child.draw()        

