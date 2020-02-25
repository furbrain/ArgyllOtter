import pygame
import shapely.geometry as geom
import numpy as np
import vtk

from .util import make_actor

class Barrel:
    def __init__(self, pos, colour=(255,255,0), size=56, height=80):
        self.pos = np.array(pos)
        self.size = size
        self.height = height
        self.colour = np.array(colour)
        cyl = vtk.vtkCylinderSource()
        cyl.SetHeight(self.height)
        cyl.SetRadius(self.size / 2)
        cyl.SetResolution(20)
        cyl.SetCenter(0, self.height/2, 0)
        self.actor = make_actor(cyl)
        self.actor.GetProperty().SetColor(*(self.colour / 255.0))
        self.actor.SetPosition(self.pos[0], 0, self.pos[1])
        self.grabber = None
        
        
    def grab(self, grabber):
        if np.hypot(*(grabber.get_pos()-self.pos)) < self.size:
            self.grabber = grabber
        
    def release(self, grabber):
        if self.grabber==grabber:
            self.grabber = None
        
    def get_pos(self):
        if self.grabber:
            self.pos = self.grabber.get_pos()
            self.actor.SetPosition(self.pos[0], 0, self.pos[1])
        return self.pos
        
    def get_shape(self):
        pt = geom.Point(self.get_pos())
        return pt.buffer(self.size/2).exterior
        
    def draw(self, arena):
        pygame.draw.circle(arena.screen, 
                           self.colour, 
                           [int(x) for x in self.get_pos() * arena.SCALE], 
                           int(self.size * arena.SCALE / 2))
                           
    def get_actor(self):
        self.get_pos()
        return self.actor
