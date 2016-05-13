import gui
import pygame


class Window(gui.Gui):
    def __init__(self, area):
        gui.Gui.__init__(self)
        self.area = area
        self.stack = None

    def draw(self, surface):
        self.stack.draw_background(surface)
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
        self.background = None

    def open(self, win):
        self.background = None
        win.stack = self
        self.windows.append(win)

    def close(self, win=None):
        self.background = None
        if win:
            self.windows.remove(win)
        else:
            self.windows.pop()

    def draw_background(self, surface):
        if not self.background:
            self.background = pygame.Surface(surface.get_size())
            self.base_gui.draw(self.background)
            for w in self.windows[:-1]:
                w.draw(self.background)
            self.background.set_alpha(50)

        surface.fill(pygame.Color('black'))
        surface.blit(self.background, (0, 0))

    @property
    def top(self):
        if self.windows:
            return self.windows[-1]
        else:
            return self.base_gui
