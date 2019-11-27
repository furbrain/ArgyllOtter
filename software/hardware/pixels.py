import rpi_ws281x

PIN=13
def Pixels(num_pixels=12):
    strip = rpi_ws281x.PixelStrip(num_pixels, PIN, channel=1)
    strip.begin()
    return strip
