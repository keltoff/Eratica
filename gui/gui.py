import coords

class Gui:
    def __init__(self):
        self.parts = []

    def draw(self, surface):
        for part in self.parts:
            part.draw(surface)

    def process_event(self, event):
        relevant = True  #hack

        for part in self.parts:
            if relevant:
                part.process_event(event)

    def add(self, new_part):
        self.parts.append(new_part)

    def get_part_at(self, pos):
        for part in self.parts:
            if part.area.collidepoint(pos):
                return part

        return None

    def get_cursor_at(self, pos):
        part = self.get_part_at(pos)
        if part:
            return part.get_cursor(coords.Coord(pos) - part.area.topleft)
        else:
            return None
