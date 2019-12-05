#!/usr/bin/env python3
import pygame
import asyncio

from .shetty import Shetty
from .drivetrain import Drive

class Arena:
    def __init__(self, size=(640,480), bg=(0,0,0)):
        self.size = size
        self.bg = bg
        pygame.init()
        pygame.display.set_caption("Shetty Simulator")
        self.screen = pygame.display.set_mode(size)
        self.objects = []
        
    def add_object(self, obj):
        self.objects.append(obj)

    async def pygame_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    return
            self.screen.fill(self.bg)
            for obj in self.objects:
                obj.draw(self.screen)
            pygame.display.flip()
            await asyncio.sleep(0.03)


     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    a = Arena()
    s = Shetty(pos=(3200,2400))
    a.add_object(s)
    d = Drive(s)
    async def test():
       await d.a_goto(600,1000)
       await asyncio.sleep(0.5)
       await d.spin(-90, 100)
       await asyncio.sleep(0.5)
       await d.a_goto(600,1000)
       await asyncio.sleep(0.5)
       d.stop()
    # call the main function
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(test())
    loop.run_until_complete(a.pygame_loop())
