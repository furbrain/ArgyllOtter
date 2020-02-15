#!/usr/bin/env python3
import time
import numpy as np
import pygame
import shapely.geometry as geom
import vtk

class Shetty:
    def __init__(self, pos = None, direction = 0):
        if pos is None:
            self.pos = np.array((0.0, 0.0), dtype='float64')
        else:
            self.pos = np.array(pos, dtype='float64')       
        self.direction = direction
        self.speed = 0
        self.angular_velocity = 0
        self.last_now = time.time()
        self.laser = False
        self.width = 200
        self.length = 300 
        self.colour = (0,255,0)
        self.distance_counter = 0
        self.camera = vtk.vtkCamera()
        self.camera.SetClippingRange(1,10000)
        self.camera.SetViewUp(0, 1, 0)
        self.camera.SetViewAngle(41.41)
        self.update_camera()
                
    def move(self, speed):
        self.speed = speed
        
    def spin(self, rate):
        self.angular_velocity = rate

    def stop(self):
        self.speed = 0
        self.angular_velocity = 0
        
    def reset_position(self):
        self.distance_counter = 0
        
    def get_coeffs(self):    
        radians = self.direction * np.pi / 180
        return np.array((np.sin(radians), np.cos(radians)))
        
    def update_camera(self):
        pos = self.pos + self.get_coeffs()*150
        focus = self.pos + self.get_coeffs()*250
        self.camera.SetFocalPoint(focus[0], 100, focus[1])
        self.camera.SetPosition(pos[0], 100, pos[1])
        self.camera.SetViewUp(0,1,0)
        #self.camera.ComputeViewPlaneNormal()

    def update(self, now=None):
        if now is None:
            now = time.time()
        dt = now-self.last_now
        self.last_now = now
        self.direction -= self.angular_velocity * dt
        coeffs  = np.array(self.get_coeffs())
        distance = self.speed * dt
        self.distance_counter += distance
        self.pos += coeffs * distance
        self.update_camera()
        
    def get_corners(self):
        s, c = self.get_coeffs()
        R = np.array([[c, s], [-s, c]])
        corners = np.array([[-self.width, self.length],
                            [self.width, self.length],
                            [self.width, -self.length],
                            [-self.width, -self.length]]) / 2
        corners = corners @ R.T
        corners += self.pos
        return corners
        
    def get_shape(self):
        return geom.LinearRing(self.get_corners())
        
    def get_front(self, offset):
        line = geom.LineString([self.pos, self.pos + self.get_coeffs()*10000.0])
        front = line.interpolate(self.length/2 + offset)
        return front
        
    def get_laser_line(self, arena):
        start = self.get_front(0.001)
        laser_line = geom.LineString([start, self.pos + self.get_coeffs()*10000.0])
        shapes = [x.get_shape() for x in arena.objects]
        intersections = [laser_line.intersection(x) for x in shapes if x is not None]
        distance = min(start.distance(x) for x in intersections if not x.is_empty)
        end = laser_line.interpolate(distance)
        laser_line = geom.LineString((start, end)) 
        return laser_line
        
    def get_camera(self):
        return self.camera 
                
    def get_distance(self, arena):
        return self.get_laser_line(arena).length
        
    def draw(self, arena):
        self.update()
        corners = self.get_corners()
        if self.laser:
            laser_line = self.get_laser_line(arena)
            coords = np.array(laser_line)
            pygame.draw.line(arena.screen, (255,0,0), coords[0] * arena.SCALE, coords[1] * arena.SCALE)
        pygame.draw.polygon(arena.screen, self.colour, corners * arena.SCALE)
        
        
if __name__=="__main__":
    s = Shetty()
    print(s)
    s.move(10)
    for i in range(10):
        s.update()
        print(s)
        time.sleep(0.1)
    s.stop()
    s.spin(90)
    for i in range(5):
        s.update()
        print(s)
        s.draw(None)
        time.sleep(0.1)
    s.stop()
    print(s)
    s.move(10)
    for i in range(10):
        s.update()
        print(s)
        time.sleep(0.1)
    s.stop()
