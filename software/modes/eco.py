import asyncio
import pyvisgraph as vg
import cv2
import numpy as np
import pygame

import shapely.geometry as geom
import shapely.ops as ops
import shapely.affinity as affinity

from modes import mode
from compute import vision
from util import spawn

TURN_SPEED = 100
DRIVE_SPEED = 800

def draw_cross(surface, colour, pos, size, width=1):
    x = pos[0]
    y = pos[1]
    colour = pygame.Color(colour)
    pygame.draw.line(surface, colour, [x-size, y-size], [x+size, y+size], width)
    pygame.draw.line(surface, colour, [x-size, y+size], [x+size, y-size], width)
    
def get_visgraph(points_list):
    graph = vg.VisGraph()
    graph.build(points_list, workers=3, status=False)
    return graph

def angle_over(target, angle):
    while target > angle:
        angle += 360
    if angle < target + 90:
        return True
    return False
    
class Retrieve(mode.Mode):
    HARDWARE = ('drive','camera','laser','grabber')
        
    async def run(self):
        self.grabber.open()
        await asyncio.sleep(1)
        image = self.camera.get_image()
        cv2.imwrite("fred.jpg", image)
        positions = await vision.find_objects(self.camera, "red", 56)
        nearest = min(positions, key = lambda x: x[1], default=(0,0))
        await self.drive.spin(nearest[0], 20)
        dist = await self.laser.get_distance()
        await self.drive.a_goto(400, dist-50)
        await asyncio.sleep(2)

class Process(mode.Mode):
    HARDWARE = ('drive','camera','laser','grabber', 'display')
    
    def on_start(self):
        self.pos =np.array((1100, 1800), dtype="float64")
        self.azimuth = 270 #"north", in degrees
        self.barrel_map = []
        self.route = []
        self.blockages = []
        
    def get_coeffs(self, bearing=None):
        if bearing is None:
            bearing = self.azimuth
        radians = bearing * np.pi / 180
        return np.array((np.cos(radians), np.sin(radians)))
        
    async def set_azimuth(self, azimuth):
        azimuth %= 360
        turn = azimuth - self.azimuth
        if turn < -180:
            turn  = turn + 360
        if turn > 180:
            turn  = turn - 360
        await self.turn(turn)
        
        
    async def turn(self, angle, speed=TURN_SPEED):
        true_angle = await self.drive.spin(angle, speed, accurate=True)
        self.azimuth += true_angle
        self.azimuth %= 360
        
    async def goto(self, distance, speed=DRIVE_SPEED):
        if distance < 0:
            speed = -speed
        distance = await self.drive.a_goto(speed, distance, accurate=True)
        self.pos += self.get_coeffs() * distance
        
    def correct_barrel(self, barrel):
        angle, distance, colour = barrel
        opposite = np.tan(np.deg2rad(angle)) * distance
        distance += 150
        theta = np.rad2deg(np.arctan2(opposite, distance))
        return (theta, distance, colour)
        
    async def find_barrels(self):
        tasks = [vision.find_objects(self.camera, x, 56) for x in ("red","green")]
        reds, greens = await asyncio.gather(*tasks)
        barrels = [(angle, distance, "red") for angle, distance in reds]
        barrels += [(angle, distance, "green") for angle, distance in greens]
        barrels = [self.correct_barrel(b) for b in barrels]
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
         
    async def create_map(self, start_angle, finish_angle, reverse=False, thorough=False):
        self.display.draw_text("Mapping")
        targeted = False
        first = True
        #FIXME - save copy of barrel map and use to update position...
        self.barrel_map = []
        #find most leftward barrels
        await self.set_azimuth(start_angle)
        min_distance = 10000
        while not angle_over(finish_angle, self.azimuth):
            barrels = await self.find_barrels()
            if targeted:
                barrels = list(filter(lambda x: x[0] > 2, barrels))
            elif not first:
                barrels = list(filter(lambda x: x[0] > -13, barrels))
            first = False
            for target in sorted(barrels):
                rough_pos = self.pos + self.get_coeffs() * target[1]
                if thorough or (rough_pos[1] < min_distance*1.2):
                    await self.turn(target[0])
                    speed = TURN_SPEED/2
                    while True:
                        adjustment = await self.check_centred(target[2])
                        if adjustment == 0:
                            break
                        await self.turn(adjustment, speed=speed)
                        speed /= 2
                    distance = await self.laser.get_distance()
                    targeted = True
                    pos = self.pos + self.get_coeffs() * (distance+150)
                    if pos[1]>250:
                        self.barrel_map.append((pos, target[2]))
                        min_distance = min(min_distance, pos[1])
                    break
            else:
                await self.turn(15)
                targeted = False
                
    async def create_visibility_graph(self, barrels):
        self.display.draw_text("Planning")
        self.blockages = []
        for pos, colour in barrels:
            pt = geom.Point(pos).buffer(200, resolution=2)
            self.blockages.append(pt)
        blockages = ops.unary_union(self.blockages)
        if isinstance(blockages, geom.polygon.Polygon):
            blockages = [blockages]
        vg_points = [[vg.Point(x,y) for x,y in pts.exterior.coords] for pts in blockages]
        self.graph = await spawn(get_visgraph, vg_points)
                
    def calculate_route(self, destination):
        route = self.graph.shortest_path(vg.Point(*self.pos), vg.Point(*destination))
        self.route = np.array([[p.x, p.y] for p in route])
        
    async def follow_route(self, shorten=0):
        self.display.draw_text("Storing")
        for waypoint in self.route[1:]:
            offset = waypoint - self.pos
            bearing = np.rad2deg(np.arctan2(offset[1], offset[0]))
            distance = np.hypot(*offset)
            if np.allclose(waypoint,self.route[-1]):
                distance -= shorten
            await self.set_azimuth(bearing)
            await self.goto(distance)
           
    def get_nearest_barrel(self):
        mapped = [(np.hypot(*(pos-self.pos)), i, (pos,colour)) for i,(pos, colour) in enumerate(self.barrel_map)]
        barrel = min(mapped)
        del self.barrel_map[barrel[1]]
        return (barrel[2])            
        
    def get_highest_barrel(self):
        self.barrel_map = sorted(self.barrel_map, key= lambda x: x[0][1])
        barrel = self.barrel_map.pop(0)
        return barrel
        
    async def retrieve_barrel(self, barrel):
        self.display.draw_text("Hunting")
        self.grabber.open()
        pos = barrel[0]
        offset = pos-self.pos
        bearing = np.rad2deg(np.arctan2(offset[1], offset[0]))
        distance = np.hypot(*offset)
        if distance > 500:
            distance -= 150 + 30 + 150
        else:    
            distance -= 150 + 30 + 100
        await self.set_azimuth(bearing)
        await self.goto(distance)
        while True:
            targets = await self.find_barrels()
            print("Retrieving")
            print(targets)
            target = min(targets, key= lambda x: x[1])
            if abs(target[0] < 3):
                break
            await self.turn(target[0], speed=TURN_SPEED/2)
        distance = await self.laser.get_distance()
        await self.goto(distance - 20)
        self.grabber.close()
        return target[2]
        
    def draw(self, arena):
        for pos, colour in self.barrel_map:
            pos = [int(x) for x in pos * arena.SCALE]
            draw_cross(arena.screen, colour, pos, 10)
        for blockage in self.blockages:
            b = affinity.scale(blockage, xfact=arena.SCALE, yfact=arena.SCALE, origin = (0,0))
            pygame.draw.lines(arena.screen, (128,128,128), True, b.exterior.coords)
        if len(self.route)>0:
            scaled_route = np.array(self.route)*arena.SCALE
            pygame.draw.lines(arena.screen, (255,255,0), False, scaled_route)
        
    async def run(self):
        red_count=0
        green_count=0
        await self.goto(-100.0)
        first = True
        while (True):
            if first:
                await self.create_map(180,360, thorough=True)
                target = self.get_nearest_barrel()
                first=False
            else:
                await self.create_map(0, 180)  
                if len(self.barrel_map)==0:
                    break
                target = self.get_highest_barrel()            
            colour = await self.retrieve_barrel(target)
            await self.create_visibility_graph(self.barrel_map)
            if (colour=="green") :
                destination = (450+green_count*100,100)
                green_count += 1
            else:
                destination = (1750-red_count*100,100)
                red_count += 1
            self.calculate_route(destination)
            await self.follow_route(shorten=170)
            self.grabber.open()
            await asyncio.sleep(0.5)
            await self.goto(-100)
        self.route = [[1100,1000]]
        await self.follow_route(shorten=0)
        await self.drive.dance()
