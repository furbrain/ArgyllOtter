#!/usr/bin/env python3
import pygame
import asyncio
import shapely.geometry as geom
import numpy as np
import vtk
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "640,0"


from .util import make_actor
from .shetty import Shetty

class Walls:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        width = self.b[0] - self.a[0]
        length = self.b[1] - self.a[1]
        height = 300
        depth = 10
        dims = (
            (-depth, width+depth, 0, height, length, length+depth),
            (-depth, width+depth, 0, height, -depth, 0),
            (-depth, 0, 0, height, -depth, length+depth),
            (width, width+depth, 0, height, -depth, length+depth),
            (-depth, width+depth, -depth, 0, -depth, length+depth)
        )
       
        self.assembly = vtk.vtkAssembly()
        for d in dims:
            cube = vtk.vtkCubeSource()
            cube.SetBounds(d)
            actor = make_actor(cube)
            actor.GetProperty().SetColor(0.1, 0.1, 0.1)  
            self.assembly.AddPart(actor)
        
    def get_shape(self):
        ls = geom.LinearRing(((self.a[0], self.a[1]),
                                (self.a[0], self.b[1]),
                                (self.b[0], self.b[1]),
                                (self.b[0], self.a[1]),
                                ))
        return ls
        
    def draw(self, arena):
        pygame.draw.rect(arena.screen, (255, 255, 255), (self.a * arena.SCALE, self.b * arena.SCALE), 1)
        
    def get_actor(self):
        return self.assembly
        
        
class Arena:
    SCALE = 0.2
    def __init__(self, size=(2200,2200), bg=(0,0,0), mode=None):
        self.size = np.array(size)
        self.bg = bg
        pygame.init()
        pygame.display.set_caption("Shetty Simulator")
        self.screen = pygame.display.set_mode([int(x) for x in self.size * self.SCALE])
        self.walls = Walls(np.array((0,0)), self.size)
        self.objects = []
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground( 0.5, 0.5, 0.5 )
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.AddRenderer(self.ren)
        self.renwin.SetSize(640, 480)
        self.image = vtk.vtkWindowToImageFilter()
        self.image.SetInput(self.renwin)
        self.image.SetInputBufferTypeToRGBA()
        self.image.ReadFrontBufferOff()
        self.image.Update()
        self.camera = None
        #do ambient lighting
        for i in (-0.5, 0.5):
            for j in(-0.5, 0.5):
                light = vtk.vtkLight()
                light.SetPosition(0,2,0)
                light.SetFocalPoint(i,0,j)
                self.ren.AddLight(light)
        self.add_object(self.walls)
        if mode:
            if hasattr(mode, 'draw'):
                self.add_object(mode)
        self.shetty = None
        
    def make_shetty(self):
        self.shetty = Shetty()
        
    def get_shetty(self):
        if self.shetty is None:
            self.make_shetty()
            self.add_object(self.shetty)
        return self.shetty
    
    def get_image(self):
        return self.image.GetOutput()
        
    def add_object(self, obj):
        self.objects.append(obj)
        if hasattr(obj, 'get_actor'):
            self.ren.AddActor(obj.get_actor())
        if hasattr(obj, 'get_camera'):
            self.camera = obj.get_camera()
            
    def poll(self):
        """ called every few seconds """
        pass

    async def pygame_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    return
            self.screen.fill(self.bg)
            for obj in self.objects:
                obj.draw(self)
            pygame.display.flip()
            self.ren.SetActiveCamera(self.camera)
            self.renwin.Render()
            self.image.Modified()
            self.image.Update()
            self.poll()
            await asyncio.sleep(0.03)        

