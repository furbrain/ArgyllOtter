import numpy as np
import vtk
import pygame

from .arena import Arena
from .barrel import Barrel
from .util import make_actor
from .shetty import Shetty

START_POS = np.array((0, 400))
class Line:
    def __init__(self, start, end, colour):
        depth = 0.2
        width = 19
        self.colour = np.array(colour)
        self.start = np.array(start)
        self.end = np.array(end)
        self.assembly = vtk.vtkAssembly()
        cube = vtk.vtkCubeSource()
        length = np.hypot(*(self.start-self.end))
        cube.SetBounds(-width/2, width/2, 0, 0.1, -length/2, length/2)
        actor = make_actor(cube)
        actor.RotateY(np.rad2deg(np.arctan2(*(self.end-self.start).T)))
        centre = (self.start+self.end)/2
        actor.SetPosition(centre[0], 0, centre[1])
        actor.GetProperty().SetColor(self.colour/255)  
        self.assembly.AddPart(actor)
                            
    def draw(self, arena):
        pygame.draw.line(arena.screen, 
                         self.colour, 
                         (self.start * arena.SCALE), 
                         (self.end * arena.SCALE), 
                         1)
        
    def get_actor(self):
        return self.assembly
        
    def get_shape(self):
        return None

class LavaArena(Arena):
    SCALE=0.1
    def __init__(self):
        super().__init__(size=(7000,1500))
        self.add_object(Line((500,400),(2500,400), (255,255,255)))
        self.add_object(Line((2500,400),(3000,900), (255,255,255)))
        self.add_object(Line((3000,900),(4000,900), (255,255,255)))
        self.add_object(Line((4000,900),(4500,400), (255,255,255)))
        self.add_object(Line((4500,400),(6500,400), (255,255,255)))
    
    def make_shetty(self):
        print("Make the Lava Shetty")
        self.shetty = Shetty(pos = START_POS, direction=88)
        
    
