from modes import mode
import asyncio
from compute import vision
import cv2
import numpy as np
from matplotlib import pyplot as plt
from util import spawn


DRIVE_SPEED = 600
TURN_SPEED = DRIVE_SPEED * 0.8

class Lava(mode.Mode):
    HARDWARE = ('drive','camera')
    TURNS = "rllr"    
    async def find_lines(self):
        img = self.camera.get_image()
        img = img[240:,:]
        return await spawn(vision.find_lines,img)
        
    def veer_left(self):
        self.drive.drive(TURN_SPEED, DRIVE_SPEED)

    def veer_right(self):
        self.drive.drive(DRIVE_SPEED, TURN_SPEED)

    def go_straight(self):
        self.drive.drive(DRIVE_SPEED)
        
    def get_current_line(self, lines):
        matches = []
        for x1,y1,x2,y2,angle,rho in lines:     
            if -40 < angle < 40:
                if y1 > 220:
                    matches.append([angle, x1, y2])
                elif y2 > 220:       
                    matches.append([angle, x2, y1])
        if len(matches) == 0:
            return None, None, None
        elif len(matches) == 1:
            return matches[0]
        elif len(matches) == 2:
            return np.mean(matches, axis=0)
        else:
            left = np.array(min(matches))
            right = np.array(max(matches))
            return (left+right)/2

    def line_ends_at_centre(self, lines):
        x1,y1,x2,y2,angle,rho = lines.T
        end1 = (240 < x1) & (x1 < 400) & (y1 > 180)
        end2 = (240 < x2) & (x2 < 400) & (y2 > 180)
        return end1 | end2
            
    def get_next_line(self, lines, direction):
        matches = []
        x1,y1,x2,y2,angle,rho = lines.T
        if direction=="r":
            matches = np.logical_and(-80 < angle, angle < -20)
        else:
            matches = np.logical_and(20 < angle, angle < 80)
        matches = np.logical_and(matches, self.line_ends_at_centre(lines))
        if not any(matches):
            return None, None
        matches = lines[matches]
        x1,y1,x2,y2,angle,rho = matches.T
        if direction=="r":
            startx = np.minimum(x1,x2)
            endx = np.maximum(x1,x2)
        else:
            startx = np.maximum(x1,x2)
            endx = np.minimum(x1,x2)
        starty = np.maximum(y1,y2)
        endy = np.minimum(y1,y2)
        start = self.camera.get_position(np.mean(startx),np.mean(starty)+240)
        end = self.camera.get_position(np.mean(endx),np.mean(endy)+240)
        vector = end-start
        angle = np.arctan2(vector[1],vector[0])
        return np.rad2deg(angle), start[1]
        
    async def follow_line(self, direction):
        while True:
            last_distance=180
            lines = await self.find_lines()
            angle, pos, distance = self.get_current_line(lines)
            if angle is None:
                angle, _ = self.get_next_line(lines, direction)
                return angle, last_distance
            last_distance = distance
            if 240 < pos < 400:
                if angle < -10:
                    self.veer_left()
                elif angle > 10:
                    self.veer_right()
                else:
                    self.go_straight()
            elif pos < 240:
                self.veer_left()
            elif pos > 400:
                self.veer_right()
            
    async def run(self):
        self.drive.drive(DRIVE_SPEED)
        while True:
            lines = await self.find_lines()
            current,_,_ = self.get_current_line(lines)
            if current is not None:
                break
        for direction in self.TURNS:
            angle, distance = await self.follow_line(direction)
            if distance is not None:
                await self.drive.a_goto(DRIVE_SPEED, distance, fast=True)
            else:
                print("guessing")
                await self.drive.a_goto(DRIVE_SPEED, 100, fast=True)
            if direction=="r":
                await self.drive.fast_turn(45, TURN_SPEED)
            else:
                await self.drive.fast_turn(-45, TURN_SPEED)
            while True:
                break
                lines = await self.find_lines()
                current,_,_ = self.get_current_line(lines)
                if current is not None:
                    break                 
            self.drive.drive(DRIVE_SPEED)
        await self.follow_line("r")            
        await self.drive.a_goto(DRIVE_SPEED,700)
        self.drive.stop()

