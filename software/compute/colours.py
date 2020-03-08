import settings


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class Colours(settings.Settings):
    def default(self):
        self.red = ([-10, 80, 30], [10, 255, 255])
        self.yellow = ([25, 120, 30], [35, 255, 255])
        self.green = ([50, 80, 30], [70, 255, 255])
        self.blue = ([110, 50, 30], [130, 255, 255])

    def get_colour(self, text):
        return getattr(self, text)
