#!/usr/bin/env python3
import numpy as np
import pygame
import pyvisgraph as vg
import shapely.affinity as affinity
import shapely.geometry as geom
import shapely.ops as ops

from util import get_coeffs, spawn


def get_visgraph(points_list):
    graph = vg.VisGraph()
    graph.build(points_list, workers=3, status=False)
    return graph


def draw_cross(surface, colour, pos, size, width=1):
    x = pos[0]
    y = pos[1]
    colour = pygame.Color(colour)
    pygame.draw.line(surface, colour, [x - size, y - size], [x + size, y + size], width)
    pygame.draw.line(surface, colour, [x - size, y + size], [x + size, y - size], width)


class Barrel:
    def __init__(self, pos, colour, precise):
        self.pos = pos
        self.colour = colour
        self.precise = precise

    def __str__(self):
        return "Barrel: <%s, %s, %s>" % (self.pos, self.colour, self.precise)

    def __repr__(self):
        return str(self)

    @staticmethod
    def fromPolar(origin, azimuth, distance, colour, precise=True):
        pos = origin + get_coeffs(azimuth) * distance
        return Barrel(pos, colour, precise)

    @staticmethod
    def fromCamera(origin, azimuth, angle, distance, colour):
        b = Barrel.fromPolar(origin, azimuth + angle, distance, colour, False)
        return b

    def get_distance(self, pos):
        return np.hypot(*(self.pos) - pos)

    def get_relative_bearing(self, origin, azimuth):
        pos = self.pos - origin
        angle = np.rad2deg(np.arctan2(pos[0], pos[1]))
        angle -= azimuth
        if angle > 180:
            return angle - 360
        elif angle < -180:
            return angle + 360
        else:
            return angle

    def in_bounds(self):
        # maybe adjust for less precise to give more leeway...
        if 200 < self.pos[0] < 2000:
            if 200 < self.pos[1] < 1950:
                return True
        return False

    def draw(self, arena):
        pos = [int(x) for x in self.pos * arena.SCALE]
        height = arena.screen.get_height()
        pos[1] = height - pos[1]
        draw_cross(arena.screen, self.colour, pos, 10)

    def near(self, other):
        if self.colour == other.colour:
            offset = self.pos - other.pos
            distance = np.hypot(*offset)
            if distance < 350:
                return distance
        return False

    def nearest(self, lst):
        contenders = [b for b in lst if b.near(self)]
        if contenders:
            return min(contenders, key=lambda b: b.near(self))
        return None


class BarrelMap:
    def __init__(self):
        self.barrels = []
        self.blockages = []

    def __str__(self):
        text = "\n            ".join(str(b) for b in self.barrels)
        return "Barrel Map: " + text

    def add(self, barrel):
        self.barrels.append(barrel)

    def remove(self, barrel):
        self.barrels.remove(barrel)

    def empty(self):
        return len(self.barrels) == 0

    def clear(self):
        self.barrels = []

    def get_nearest(self, pos):
        barrel = min(self.barrels, key=lambda x: np.hypot(*(x.pos - pos)))
        return barrel

    def get_highest(self):
        barrel = max(self.barrels, key=lambda x: x.pos[1])
        return barrel

    async def calculate_route(self, start, destination):
        self.blockages = []
        for barrel in self.barrels:
            pt = geom.Point(barrel.pos).buffer(200, resolution=2)
            self.blockages.append(pt)
        self.blockages = ops.unary_union(self.blockages)
        if isinstance(self.blockages, geom.polygon.Polygon):
            self.blockages = [self.blockages]
        vg_points = [[vg.Point(x, y) for x, y in pts.exterior.coords] for pts in self.blockages]
        graph = await spawn(get_visgraph, vg_points)
        route = graph.shortest_path(vg.Point(*start), vg.Point(*destination))
        route = np.array([[p.x, p.y] for p in route])
        return route

    def known(self, barrel):
        return barrel.nearest(self.barrels)

    def count(self, colour):
        return len([b for b in self.barrels if b.colour == colour])

    def draw(self, arena):
        h = arena.screen.get_height()
        for barrel in self.barrels:
            barrel.draw(arena)
        for blockage in self.blockages:
            b = affinity.scale(blockage, xfact=arena.SCALE, yfact=arena.SCALE, origin=(0, 0))
            b = affinity.scale(b, xfact=1, yfact=-1, origin=(0, h / 2))
            pygame.draw.lines(arena.screen, (128, 128, 128), True, b.exterior.coords)
