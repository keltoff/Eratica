import pygame.font

class Gui:
    def __init__(self):
        self.parts = []

        pygame.font.init()
        self.font = pygame.font.SysFont('default', 50)


    def draw(self, surface):
        for part in self.parts:
            part.draw(surface)
        surface.blit(self.font.render('{}'.format(pygame.mouse.get_pos()), True, (0, 200, 0)), (50, 420))

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
            return part.get_cursor(pos)
        else:
            return None
