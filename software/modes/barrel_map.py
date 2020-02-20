#!/usr/bin/env python3
import numpy as np
import pyvisgraph as vg
import shapely.geometry as geom
import shapely.ops as ops
import shapely.affinity as affinity



def get_visgraph(points_list):
    graph = vg.VisGraph()
    graph.build(points_list, workers=3, status=False)
    return graph


class Barrel:
    def __init__(self, pos, colour, precise):
        self.pos = pos
        self.colour = colour
        self.precise = precise
    
    @staticmethod    
    def fromPolar(origin, azimuth, distance, colour, precise=True):
        pos = origin + get_coeffs(azimuth) * distance
        return Barrel(pos, colour, precise)
        
    @staticmethod
    def fromCamera(origin, azimuth, angle, distance, colour):
        b = Barrel.fromPolar(origin, azimuth+angle, distance, colour, False)
        offset = get_coeffs(azimuth) * CAMERA_OFFSET
        b.pos  += offset
        return b
        
    @staticmethod
    async def fromImage(camera, origin, azimuth):
        image = camera.get_image()
        tasks = [vision.find_objects(camera, col, 56, image) for col in ("red","green")]
        reds, greens = await asyncio.gather(*tasks)
        barrels = [Barrel.fromCamera(origin, azimuth, angle, distance, "red") for angle, distance in reds]
        barrels += [Barrel.fromCamera(origin, azimuth, angle, distance, "green") for angle, distance in greens]
        return barrels
        
    def get_relative_bearing(self, origin, azimuth):
        pos = self.pos - origin
        angle = np.rad2deg(np.arctan2(pos[1], pos[0]))
        angle -= azimuth
        if angle >180:
            return angle - 360
        elif angle < -180:
            return angle + 360
        else:
            return angle
                
    def in_bounds(self):
        #maybe adjust for less precise to give more leeway...
        if 200 < self.pos[0] < 2000:
            if 250 < self.pos[1] < 2000:
                return True
        return False


    def draw(self, arena):
        pos = [int(x) for x in self.pos * arena.SCALE]
        draw_cross(arena.screen, self.colour, pos, 10)
    
class BarrelMap(self):
    def __init__(self):
        self.barrels = []
        self.blockages = []
        
    def add(self, barrel):
        self.barrels.append(barrel)

    def del(self, barrel):
        self.barrels.remove(barrel)
        
    def get_nearest(self):
        barrel = min(self.barrels, key= lambda x: np.hypot(*(x.pos-pos)))
        return barrel
        
    def get_highest(self):
        barrel = max(self.barrels, key= lambda x: x.pos[1])
        return barrel
        
    async def calculate_route(self, start, destination):
        self.blockages = []
        for barrel in self.barrels:
            pt = geom.Point(barrel.pos).buffer(200, resolution=2)
            self.blockages.append(pt)
        self.blockages = ops.unary_union(self.blockages)
        if isinstance(blockages, geom.polygon.Polygon):
            blockages = [blockages]
        vg_points = [[vg.Point(x,y) for x,y in pts.exterior.coords] for pts in blockages]
        graph = await spawn(get_visgraph, vg_points)
        route = graph.shortest_path(vg.Point(*start), vg.Point(*destination))
        route = np.array([[p.x, p.y] for p in route])
        return route
        

    def draw(self, arena):
        for barrel in self.barrels:
            barrel.draw(arena)
        for blockage in self.blockages:
            b = affinity.scale(blockage, xfact=arena.SCALE, yfact=arena.SCALE, origin = (0,0))
            pygame.draw.lines(arena.screen, (128,128,128), True, b.exterior.coords)
            
