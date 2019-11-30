import cv2
import imutil

COLOURS = {
    "red": ([-10,80,30],[10,255,255]),
    "green": ([50,80,30],[70,255,255]),
    "blue": ([110,80,30],[130,255,255]),
}

def find_all_contours(image, colour_name="red", colour_arrays=None):
    if colour_arrays is None:
        colour_arrays = COLOURS[colour_name]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    least_hue = colour_arrays[0][0]
    lower = np.array(colour_arrays[0], dtype = "uint8")
    upper = np.array(colour_arrays[1], dtype = "uint8")
    if least_hue < 0: # rotate colour space so all is positive
        hsv_image += np.array([-least_hue,0,0], dtype = "uint8")
        hsv_image[:,:,0] = np.mod(hvs[:,:,0], 180)
        lower[0] = 0
        upper[0] += -least_hue

    mask = cv2.inRange(hsv_image, lower, upper)
    
    #get rid of random blobs	
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts


def find_biggest_contour(image, colour_name="red", colour_arrays=None):
    cnts = find_all_contours(image, colour_name, colour_arrays)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        return c
    else:
        return None


