from PIL import ImageFont

# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from oled.device import sh1106, const
# noinspection PyUnresolvedReferences
from oled.render import canvas


class Display:
    def __init__(self):
        self.oled = sh1106(port=1, address=0x3C)  # create display
        self.oled.command(const.COMSCANINC, const.SEGREMAP)  # invert it
        self.little_font = ImageFont.truetype("DejaVuSans.ttf", 16)
        self.big_font = ImageFont.truetype("DejaVuSans.ttf", 32)

    def canvas(self):
        return canvas(self.oled)

    def clear(self):
        with self.canvas() as c:
            c.rectangle(((0, 0), (128, 64)), 0, 0)

    def draw_text_on_canvas(self, text, canvas, x=None, y=None, fill=255, big=True):
        if big:
            font = self.big_font
        else:
            font = self.little_font
        size = canvas.textsize(text, font=font)
        if x is None:  # centre on x-axis
            x = max(0, (128 - size[0]) // 2)
        if y is None:  # centre on y-axis
            y = max(0, (64 - size[1]) // 2)
        canvas.text((x, y), text, font=font, fill=fill)

    def draw_text(self, text, x=None, y=None, fill=255, big=True, clear=True):
        with self.canvas() as c:
            if clear:
                c.rectangle(((0, 0), (128, 64)), 0, 0)
            self.draw_text_on_canvas(text, c, x, y, fill, big)
