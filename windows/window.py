import gui
import pygame


class Window(gui.Gui):
    def __init__(self, area):
        gui.Gui.__init__(self)
        self.area = area
        self.stack = None

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('green'))
        self.background.set_alpha(100)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        win_surface = surface.subsurface(self.area)
        win_surface.fill(pygame.Color('black'))
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


class WinStack:
    def __init__(self, base_gui):
        self.base_gui = base_gui
        self.windows = []

    def open(self, win):
        win.stack = self
        self.windows.append(win)

    def close(self, win=None):
        if win:
            self.windows.remove(win)
        else:
            self.windows.pop()

    def build_background(self):
        pass

    @property
    def top(self):
        if self.windows:
            return self.windows[-1]
        else:
            return self.base_gui
