import time
import vtk
import pygame
import shapely.geometry as geom
import numpy as np

from .arena import Arena
from .util import make_actor
from .shetty import Shetty

class Mine:
    def __init__(self):
        depth = 0.2
        width = 400
        self.colour = np.array((255,0,0))
        self.pos = np.array((0,0))
        self.make_shape()
        self.size = np.array((width, width))
        cube = vtk.vtkCubeSource()
        cube.SetBounds((0,width,0,depth,0,width))
        self.actor = make_actor(cube)
        self.actor.GetProperty().SetColor(self.colour/255)  
            
    def draw(self, arena):
        pygame.draw.rect(arena.screen, self.colour, (self.pos * arena.SCALE, self.size * arena.SCALE))
        
    def get_actor(self):
        return self.actor
        
    def get_shape(self):
        return None
        
    def make_shape(self):
        self.shape = geom.Polygon((self.pos,
                                  self.pos + np.array((0,400)),
                                  self.pos + np.array((400,0)),
                                  self.pos + np.array((400,400))))
        
    def randomise(self):
        self.pos = np.random.randint(4, size=(2,)) * 400
        self.make_shape()
        self.actor.SetPosition(self.pos[0],0,self.pos[1])

    def on_target(self, shetty):
        return self.shape.intersects(shetty.get_shape())


class MineField(Arena):
    def __init__(self):
        super().__init__(size=(1600, 1600))
        np.random.seed(0)
        self.mine = Mine()
        self.add_object(self.mine)
        self.score = 0
        self.start_time=time.time()
        self.winning = False
    
    def make_shetty(self):
        print("setting up eco shetty")
        self.shetty = Shetty(pos = (800,800), direction=45)

    def poll(self):
        if (self.mine.on_target(self.shetty) and 
           self.shetty.speed==0 and
           self.shetty.angular_velocity==0):
            if not self.winning:
                self.start_time = time.time()
                self.winning = True
            else:
                if time.time() > self.start_time + 1:
                    self.score += 1
                    print("Score: ", self.score)
                    self.mine.randomise()
                    self.winning=False
        else:
            self.winning = False
