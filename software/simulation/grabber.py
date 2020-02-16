#!/usr/bin/env python3
import logging
from util import logged
import numpy as np
class Grabber:
    def __init__(self, shetty, arena):
        self.shetty = shetty
        self.arena = arena
            
    def get_pos(self):
        return np.array(self.shetty.get_front(30))        
            
    @logged    
    def open(self):
        for item in self.arena.objects:
            if hasattr(item, "release"):
                item.release(self)        
    
    @logged    
    def close(self):
        for item in self.arena.objects:
            if hasattr(item, "grab"):
                item.grab(self)        
    @logged
    def off(self):
        pass
        
    def set_positions(self, opened, closed):
        pass
