import cv2
import imutils
import numpy as np
import asyncio
from util import spawn
import time

COLOURS = {
    "red": ([-10,80,30],[10,255,255]),
    "yellow": ([25,120,30],[35,255,255]),
    "green": ([50,80,30],[70,255,255]),
    "blue": ([110,50,30],[130,255,255]),
}

def find_all_contours(image, colour="red"):
    if isinstance(colour, str):
        colour_arrays = COLOURS[colour]
    else:
        colour_arrays = colour
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    least_hue = colour_arrays[0][0]
    lower = np.array(colour_arrays[0], dtype = "uint8")
    upper = np.array(colour_arrays[1], dtype = "uint8")
    if least_hue < 0: # rotate colour space so all is positive
        hsv_image += np.array([-least_hue,0,0], dtype = "uint8")
        hsv_image[:,:,0] = np.mod(hsv_image[:,:,0], 180)
        lower[0] = 0
        upper[0] += -least_hue

    mask = cv2.inRange(hsv_image, lower, upper)
    
    #get rid of random blobs	
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=4)
    mask = cv2.erode(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts


def find_biggest_contour(image, colour="red"):
    cnts = find_all_contours(image, colour)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        return c
    else:
        return None


def find_lines(image, debug=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smaller = cv2.resize(gray,(315,115))
    cropped = smaller[10:-10,10:-10]
    least = np.amin(cropped)
    most = np.amax(cropped)
    smaller -=least
    smaller *= 255//most-least
    #smaller = cv2.equalizeHist(smaller)
    edges = cv2.Canny(smaller, 2000, 3000, apertureSize=5)
    if debug:
        cv2.imwrite("smaller.png", smaller)
        cv2.imwrite("edges.png", edges)
    lines = cv2.HoughLinesP(edges,1,np.pi/180, 30, np.array([]), 30,10)
    if lines is None:
        return []
    lines = lines[:,0,:]
    x1,y1,x2,y2 = lines.T
    x1*=2
    x2*=2
    y1*=2
    y2*=2
    #get angle as offset from vertical
    theta = np.arctan2(y1-y2, x1-x2)
    rho = np.sin(theta)*x1+np.cos(theta)*y1
    angle = np.rad2deg(theta) % 180
    angle %= 180
    angle -= 90
    angle *= -1
    # find duplicates, based on angle and rho
    return np.stack((x1,y1,x2,y2,angle, rho)).T


