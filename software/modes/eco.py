from modes import mode
import asyncio
from compute import vision
import cv2
import numpy as np

TURN_SPEED = 50
DRIVE_SPEED = 400

class Retrieve(mode.Mode):
    HARDWARE = ('drive','camera','laser','grabber')
        
    async def run(self):
        self.grabber.open()
        await asyncio.sleep(1)
        image = self.camera.get_image()
        cv2.imwrite("fred.jpg", image)
        positions = await vision.find_objects(self.camera, "red", 56)
        print(positions)
        nearest = min(positions, key = lambda x: x[1], default=(0,0))
        print(nearest)
        await self.drive.spin(nearest[0], 20)
        dist = await self.laser.get_distance()
        print(dist)
        await self.drive.a_goto(400, dist-50)
        print(await self.laser.get_distance())
        await asyncio.sleep(2)

class Process(mode.Mode):
    HARDWARE = ('drive','camera','laser','grabber')
    
    def on_start(self):
        self.pos =np.array((1100,1800), dtype="float64")
        self.azimuth = 0 #"north", in degrees
        self.barrel_map = []
        
    def get_coeffs(self):
        radians = self.azimuth * np.pi / 180
        return np.array((np.sin(radians), np.cos(radians)))
        
    async def turn(self, angle, speed=TURN_SPEED):
        await self.drive.spin(angle, TURN_SPEED)
        self.azimuth += angle
        print(self.azimuth)
        
    async def goto(self, distance, speed=DRIVE_SPEED):
        if distance < 0:
            speed = -speed
        await self.drive.a_goto(speed, distance)
        self.pos += self.get_coeffs() * distance
        
    async def find_barrels(self):
        tasks = [vision.find_objects(self.camera, x, 56) for x in ("red","green")]
        reds, greens = await asyncio.gather(*tasks)
        barrels = [(angle, pos, "red") for angle, pos in reds]
        barrels += [(angle, pos, "green") for angle, pos in greens]
        return barrels
        
    async def check_centred(self, colour):
        image = self.camera.get_image()
        positions = await vision.find_objects(self.camera, colour, 56)
        angles = [(abs(x[0]), x[0]) for x in positions]
        central = sorted(angles)[0]
        if central[0]<1:
            return 0
        else:
            return central[1] 
         
    async def create_map(self):
        await self.turn(-90)
        targeted = False
        first = True
        #find most leftward barrels
        while self.azimuth < 90:
            barrels = await self.find_barrels()
            if targeted:
                barrels = list(filter(lambda x: x[0] > 2, barrels))
            elif not first:
                barrels = list(filter(lambda x: x[0] > -13, barrels))
            first = False
            if len(barrels)>0:
                target = sorted(barrels)[0]
                await self.turn(target[0])
                while True:
                    distance, adjustment = await asyncio.gather(self.laser.get_distance(), self.check_centred(target[2]))
                    if adjustment == 0:
                        break
                    await self.turn(adjustment, speed=TURN_SPEED/4)
                targeted = True
                pos = self.pos + self.get_coeffs() * distance
                self.barrel_map.append((pos, target[2]))
            else:
                await self.turn(15)
                targeted = False
        print(self.barrel_map) 
        
    async def run(self):
        #map all the barrels
        await self.goto(-100.0)
        await self.create_map()
        #while there are barrels:
         #find nearest barrel
         #go to it
         #grab it
         #find path to destination
         #go there
