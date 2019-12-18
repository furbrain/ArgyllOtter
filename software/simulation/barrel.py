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
        
    def get_shape(self):
        pt = geom.Point(self.pos)
        return pt.buffer(self.size/2).exterior
        
    def draw(self, arena):
        pygame.draw.circle(arena.screen, 
                           self.colour, 
                           [int(x) for x in self.pos * arena.SCALE], 
                           int(self.size * arena.SCALE / 2))
                           
    def get_actor(self):
        return self.actor
