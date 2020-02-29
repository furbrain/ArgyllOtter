import functools

import rpi_ws281x

PIN = 13


def clear_pixels(pixels):
    for i in range(pixels.numPixels()):
        pixels.setPixelColorRGB(i, 0, 0, 0)
    pixels.show()


def Pixels(num_pixels=12):
    strip = rpi_ws281x.PixelStrip(num_pixels, PIN, channel=1)
    strip.begin()
    strip.clear = functools.partial(clear_pixels, strip)
    return strip
