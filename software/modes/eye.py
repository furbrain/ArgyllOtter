#!/usr/bin/env python3
import asyncio
import time

import cv2
import numpy as np

from compute import vision
from compute.colours import Colours
from util import spawn
from .barrels import Barrel

ZONES = {'blue': ((400, 2200), (1000, 2200)),
         'yellow': ((1200, 2200), (1800, 2200))}

BARREL_WIDTH = 56  # mm


class Ball:
    def __init__(self, camera, shetty, barrel_map):
        self.colour = Colours()
        self.camera = camera
        self.shetty = shetty
        self.barrel_map = barrel_map
        self.track_barrels = False
        self.image = None

    def find_barrels_from_contour(self, contours, colour, ignore_edges=True):
        results = []
        for c in contours:
            x_min = min(c[:, :, 0])[0]
            x_max = max(c[:, :, 0])[0]
            if ignore_edges:
                if x_min == 0:
                    print("ignoring edge case")
                    continue  # ignore as at edge of image
                if x_max >= 638:
                    print("ignoring edge case")
                    continue  # ignore as at edge of image

            centre = (x_min + x_max) / 2
            size = x_max - x_min
            angle = self.camera.pose.get_bearing(centre)
            distance = BARREL_WIDTH / np.tan(np.deg2rad(self.camera.pose.get_angle_width(size)))
            b = Barrel.fromCamera(self.shetty.pos, self.shetty.azimuth, angle, distance, colour)
            results.append(b)
        return results

    def find_zones(self, contours, colour):
        # get biggest contour
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x_min = min(c[:, :, 0])[0]
            x_max = max(c[:, :, 0])[0]
            if x_max - x_min > 30:  # make sure is a decent sized patch...
                if x_min > 2:
                    #print(colour)
                    angle = self.camera.pose.get_bearing(x_min)
                    self.shetty.observed(angle, ZONES[colour][0])
                if x_max < 478:
                    #print(colour)
                    angle = self.camera.pose.get_bearing(x_max)
                    self.shetty.observed(angle, ZONES[colour][1])

    async def look(self):
        self.image = self.camera.get_image()
        high_image = self.image[235:240, :]  # only look at middle bit for yellow and blue
        barrel_image = self.image[240:, :]
        tasks = [spawn(vision.find_all_contours, barrel_image, col) for col in (self.colour.red, self.colour.green)]
        tasks += [spawn(vision.find_all_contours, high_image, col) for col in (self.colour.yellow, self.colour.blue)]
        reds, greens, yellows, blues = await asyncio.gather(*tasks)
        self.find_zones(yellows, "yellow")
        self.find_zones(blues, "blue")
        return reds, greens

    def find_barrels(self, reds, greens, ignore_edges=True):
        barrels = self.find_barrels_from_contour(reds, "red", ignore_edges)
        barrels += self.find_barrels_from_contour(greens, "green", ignore_edges)
        return barrels

    def classify_barrels(self, barrels):
        known_barrels = []
        unknown_barrels = []
        for b in barrels:
            found = self.barrel_map.known(b)
            if found:
                known_barrels.append(found)
                if self.track_barrels:
                # print(b.colour)
                    angle = b.get_relative_bearing(self.shetty.pos, self.shetty.azimuth)
                    self.shetty.observed(angle, found.pos, b.get_distance(self.shetty.pos))
            else:
                unknown_barrels.append(b)
        return known_barrels, unknown_barrels

    async def find_and_classify_barrels(self):
        reds, greens = await self.look()
        barrels = self.find_barrels(reds, greens)
        known, unknown = self.classify_barrels(barrels)
        return known, unknown

    async def find_leftmost_unknown_barrel(self):
        """return leftmost barrel that has not been found before"""
        reds, greens = await self.look()
        barrels = self.find_barrels(reds, greens)
        known, unknown = self.classify_barrels(barrels)
        unknown = [b for b in unknown if b.in_bounds()]
        if unknown:
            b = min(unknown, key=lambda b: b.get_relative_bearing(self.shetty.pos, self.shetty.azimuth))
            return b
        return None

    async def line_up_for_laser(self, target):
        """give correction needed to line up laser on specified barrel
        note we need access to contours for this..."""
        reds, greens = await self.look()
        barrels = self.find_barrels(reds, greens, ignore_edges=False)
        # self.classify_barrels(barrels)
        contours = reds + greens
        for c, b in zip(contours, barrels):
            if b.near(target):
                x_min = min(c[:, :, 0])[0]
                x_max = max(c[:, :, 0])[0]
                if x_min < self.camera.pose.zero_degree_pixel - 5:
                    if x_max > self.camera.pose.zero_degree_pixel + 5:
                        return 0
                return b.get_relative_bearing(self.shetty.pos, self.shetty.azimuth)
        return None

    async def line_up_for_grab(self, target):
        """ give correction needed to line up on this barrel"""
        reds, greens = await self.look()
        barrels = self.find_barrels(reds, greens, ignore_edges=False)
        # self.classify_barrels(barrels)
        nearest = target.nearest(barrels)
        #print("target", target)
        #print("grab list", barrels)
        if nearest:
            return nearest.get_relative_bearing(self.shetty.pos, self.shetty.azimuth), nearest
        else:
            print("lost a barrel")
            print("expected azimuth and distance: ", target.get_relative_bearing(self.shetty.pos, self.shetty.azimuth),
                  target.get_distance(self.shetty.pos))
            print("available barrels: ")
            for b in barrels:
                print(b.get_relative_bearing(self.shetty.pos, self.shetty.azimuth), b.get_distance(self.shetty.pos))
            tm = time.time()
            filename = str(tm) + ".jpg"
            print("saving image as:", filename)
            cv2.imwrite(filename, self.image)
            return None, None

    async def just_looking(self):
        """ driving around having a looky-see, lets correct...."""
        reds, greens = await self.look()
        barrels = self.find_barrels(reds, greens)
        self.classify_barrels(barrels)
