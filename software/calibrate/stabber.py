import modes


class StabberCal(modes.Interactive):
    HARDWARE = ('stabber', 'display')

    def on_start(self):
        super().on_start()
        self.angle = 0

    def change_event(self, up):
        if up:
            self.angle += 30
        else:
            self.angle -= 30
        self.stabber.servo.set_pos(self.angle)

    def down_event(self):
        self.angle -= 30
        self.stabber.servo.set_pos(self.angle)

    async def run(self):
        self.stabber.servo.set_pos(0)
        cal = self.stabber.positions
        self.display.draw_text("Stab")
        await self.wait_for_button()
        cal.stab = self.angle
        self.display.draw_text("Release")
        await self.wait_for_button()
        cal.release = self.angle
        cal.save()
        self.display.clear()
