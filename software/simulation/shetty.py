#!/usr/bin/env python3
import time
import numpy as np
import pygame

SCALE = 0.1

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
        self.width = 200
        self.length = 300 
        self.colour = (0,255,0)
        self.distance_counter = 0
        
    def __repr__(self):
        return str(self.pos)
        
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
        return np.sin(radians), np.cos(radians)

    def update(self, now=None):
        if now is None:
            now = time.time()
        dt = now-self.last_now
        self.last_now = now
        self.direction += self.angular_velocity * dt
        coeffs  = np.array(self.get_coeffs())
        distance = self.speed * dt
        self.distance_counter += distance
        self.pos += coeffs * distance
        
    def draw(self, surface):
        s, c = self.get_coeffs()
        R = np.array([[c, s], [-s, c]])
        self.update()
        corners = np.array([[-self.width, self.length],
                            [self.width, self.length],
                            [self.width, -self.length],
                            [-self.width, -self.length]]) / 2
        corners = corners @ R.T
        corners += self.pos
        pygame.draw.polygon(surface, self.colour, corners * SCALE)
        
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
