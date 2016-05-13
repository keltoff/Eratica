import gui
import pygame
import pygame.draw

class Window(gui.Gui):
    def __init__(self, area):
        gui.Gui.__init__(self)
        self.area = area
        self.stack = None

    def draw(self, surface):
        self.stack.draw_background(surface)
        win_surface = surface.subsurface(self.area)
        win_surface.fill(pygame.Color('black'))
        pygame.draw.rect(win_surface, pygame.Color('lightblue'), win_surface.get_rect().inflate(-5, -5), 1)
        gui.Gui.draw(self, win_surface)

    def get_part_at(self, pos):
        return gui.Gui.get_part_at(self, pos - self.area.topleft)

    def close(self):
        self.stack.close(self)


class TestWindow(Window):
    def __init__(self, pos):
        Window.__init__(self, pygame.Rect(pos, (150, 150)))

        close_bt = gui.Button(pygame.Rect(10, 10, 30, 30), pygame.Color('red'))
        close_bt.click = lambda a, b: self.close()
        self.add(close_bt)
