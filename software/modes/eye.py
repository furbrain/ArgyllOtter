#!/usr/bin/env python3
import asyncio
import numpy as np
import cv2

from .barrels import Barrel
from compute import vision
from util import spawn

ZONES = {'blue' : (( 400, 2200), (1000, 2200)),
         'yellow'   : ((1200, 2200), (1800, 2200))}

BARREL_WIDTH = 56 #mm

class Ball:
    def __init__(self, camera, shetty, barrel_map):
        self.camera = camera
        self.shetty = shetty
        self.barrel_map = barrel_map
        self.track_barrels = False
        
    def find_barrels_from_contour(self, contours, colour):
        results = []
        for c in contours:
            x_min = min(c[:,:,0])[0]
            x_max = max(c[:,:,0])[0]
            if x_min == 0:
                continue #ignore as at edge of image
            if x_max >= 478:
                continue #ignore as at edge of image
        
            centre = (x_min+x_max)/2
            size = x_max-x_min
            angle = self.camera.calibration.get_bearing(centre)
            distance = BARREL_WIDTH /  np.tan(np.deg2rad(self.camera.calibration.get_angle_width(size)))
            b = Barrel.fromCamera(self.shetty.pos, self.shetty.azimuth, angle, distance, colour)
            results.append(b)
        return results
        
    def find_zones(self, contours, colour):
        #get biggest contour
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x_min = min(c[:,:,0])[0]
            x_max = max(c[:,:,0])[0]
            if x_max - x_min > 30: #make sure is a decent sized patch...
                if x_min > 2:
                    angle = self.camera.calibration.get_bearing(x_min)
                    self.shetty.observed(angle, ZONES[colour][0])
                if x_max < 478:
                    angle = self.camera.calibration.get_bearing(x_max)
                    self.shetty.observed(angle, ZONES[colour][1])
                
        
    async def look(self):
        image = self.camera.get_image()
        high_image = image[:240,:] #only look at top bit for yellow and blue
        tasks = [spawn(vision.find_all_contours, image, col) for col in ("red","green")]
        tasks += [spawn(vision.find_all_contours, high_image, col) for col in ("yellow", "blue")]
        reds, greens, yellows, blues = await asyncio.gather(*tasks)
        self.find_zones(yellows, "yellow")
        self.find_zones(blues, "blue")
        return reds, greens
        
    def find_barrels(self, reds, greens):         
        barrels = self.find_barrels_from_contour(reds,"red")
        barrels += self.find_barrels_from_contour(greens,"green")
        return barrels
        
    def classify_barrels(self, barrels):
        known_barrels = []
        unknown_barrels = []
        for b in barrels:
            found = self.barrel_map.known(b)
            if found:
                known_barrels.append(found)
                if self.track_barrels:
                    angle = b.get_relative_bearing(self.shetty.pos, self.shetty.azimuth)
                    self.shetty.observed(angle, found.pos, np.hypot(*(self.shetty.pos-b.pos)))
            else:
                unknown_barrels.append(b)
        return known_barrels, unknown_barrels
        
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
        barrels = self.find_barrels(reds, greens)
        self.classify_barrels(barrels)
        contours = reds+greens
        for c, b in zip(contours, barrels):
            if b.near(target):
                x_min = min(c[:,:,0])[0]
                x_max = max(c[:,:,0])[0]
                if x_min < self.camera.calibration.zero_degree_pixel-5:
                    if x_max > self.camera.calibration.zero_degree_pixel+5:
                        return 0
                return b.get_relative_bearing(self.shetty.pos, self.shetty.azimuth)
        return None
            
    async def line_up_for_grab(self, target):
        """ give correction needed to line up on this barrel"""
        reds, greens = await self.look()
        barrels = self.find_barrels(reds, greens)
        self.classify_barrels(barrels)
        for b in barrels:
            if b.near(target):
                return b.get_relative_bearing(self.shetty.pos, self.shetty.azimuth)
        
    async def just_looking(self):
        """ driving around having a looky-see, lets correct...."""
        reds, greens = await self.look()
        barrels = self.find_barrels(reds, greens)
        self.classify_barrels(barrels)
        
