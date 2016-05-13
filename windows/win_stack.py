import pygame


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
