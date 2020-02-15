import numpy as np
import vtk
import pygame

from .arena import Arena
from .barrel import Barrel
from .util import make_actor
from .shetty import Shetty

NUM_BARRELS = 12
START_POS = np.array((1100, 1800))
class Target:
    def __init__(self, pos, colour):
        depth = 0.2
        height = 300
        width = 600
        breadth = 200
        self.colour = np.array(colour)
        self.pos = np.array(pos)
        self.size = np.array((width, breadth))
        dims = (
            (pos[0], pos[0]+width, 0, height, pos[1], pos[1]+depth),
            (pos[0], pos[0]+width, 0, depth, pos[1], pos[1]+breadth)
        )
        self.assembly = vtk.vtkAssembly()
        for d in dims:
            cube = vtk.vtkCubeSource()
            cube.SetBounds(d)
            actor = make_actor(cube)
            actor.GetProperty().SetColor(self.colour/255)  
            self.assembly.AddPart(actor)
            
    def draw(self, arena):
        pygame.draw.rect(arena.screen, self.colour, (self.pos * arena.SCALE, self.size * arena.SCALE))
        
    def get_actor(self):
        return self.assembly
        
    def get_shape(self):
        return None

class EcoArena(Arena):
    def __init__(self):
        super().__init__(size=(2200,2200))
        np.random.seed(4)
        barrels = np.empty((0,2))
        i=0
        # do red barrels
        self.add_object(Target((400,0), (0,0,255)))
        self.add_object(Target((1200, 0), (255,255,0)))
        while i < NUM_BARRELS:    
            point = np.random.randint(300,1900,(1,2))
            try:
                distances = np.linalg.norm(barrels-point, axis=1)
            except np.AxisError:
                distances = [10000]
            if len(barrels)==0 or min(distances)>300:
                barrels = np.append(barrels, point, axis=0)
                if i % 2==0:
                    colour = (255,0,0)
                    rel_point = point[0]-START_POS
                else:
                    colour = (0,255,0)
                barrel = Barrel(point[0], colour=colour)
                self.add_object(barrel)
                i += 1
    
    def make_shetty(self):
        print("setting up eco shetty")
        self.shetty = Shetty(pos = START_POS, direction=180)
        
    
