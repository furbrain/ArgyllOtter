#!/usr/bin/env python3
import pygame
import asyncio
import shapely.geometry as geom
import numpy as np
import vtk
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "640,0"


from .util import make_actor

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
        
        
class Arena:
    SCALE = 0.2
    def __init__(self, size=(2200,2200), bg=(0,0,0)):
        self.size = np.array(size)
        self.bg = bg
        pygame.init()
        pygame.display.set_caption("Shetty Simulator")
        self.screen = pygame.display.set_mode([int(x) for x in self.size * self.SCALE])
        self.walls = Walls(np.array((0,0)), self.size)
        self.objects = []
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground( 0.5, 0.5, 0.5 )
        self.renwin = vtk.vtkRenderWindow
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.AddRenderer(self.ren)
        self.renwin.SetSize(640, 480)
        self.camera = None
        #do ambient lighting
        for i in (-0.5, 0.5):
            for j in(-0.5, 0.5):
                light = vtk.vtkLight()
                light.SetPosition(0,2,0)
                light.SetFocalPoint(i,0,j)
                self.ren.AddLight(light)
        self.add_object(self.walls)


        
    def add_object(self, obj):
        self.objects.append(obj)
        if hasattr(obj, 'get_actor'):
            self.ren.AddActor(obj.get_actor())
        if hasattr(obj, 'get_camera'):
            self.camera = obj.get_camera()

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
            await asyncio.sleep(0.03)        
        
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    from .shetty import Shetty
    from .drivetrain import Drive
    from .barrel import Barrel
    reds = np.random.randint(300,1900,(4,2))
    greens = np.random.randint(300,1900,(4,2))
    a = Arena()
    a.add_object(Target((400,0), (0,0,255)))
    a.add_object(Target((1200, 0), (255,255,0)))
    for point in reds:
        b = Barrel(point, colour=(255,0,0))
        a.add_object(b)
    for point in greens:
        b = Barrel(point, colour=(0,255,0))
        a.add_object(b)
    s = Shetty(pos=(1100,1800), direction=180)
    s.laser = True
    a.add_object(s)
    d = Drive(s)
    async def test():
       await d.a_goto(600,500)
       await asyncio.sleep(0.5)
       await d.spin(-45, 100)
       #await asyncio.sleep(0.5)
       #await d.a_goto(600,500)
       #await asyncio.sleep(0.5)
       #d.stop()
    # call the main function
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(test())
    loop.run_until_complete(a.pygame_loop())
