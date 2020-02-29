class Display:
    def __init__(self):
        self.oled = None

    def canvas(self):
        raise NotImplementedError("canvas not implemented")

    def clear(self):
        pass

    def draw_text_on_canvas(self, text, canvas, x=None, y=None, fill=255, big=True):
        print("DISPLAY: ", text)

    def draw_text(self, text, x=None, y=None, fill=255, big=True, clear=True):
        print("DISPLAY: ", text)
