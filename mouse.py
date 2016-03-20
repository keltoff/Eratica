import pygame.mouse as pm
import pygame.image as im
import pygame.draw as dr

class Mouse:
    def __init__(self, surface, cursor_set):
        pm.set_visible(False)
        #self.cursors = {None: im.load("graphics/Cursor_ST416.png").convert_alpha(surface),
        #                'hand': im.load("graphics/Cursor_GreyLight.png").convert_alpha(surface) }
        self.cursors = cursor_set
        # self.cursors = {None: (0, 0, 250),
        #                 'hand': (250, 0, 0),
        #                 'frame': (150, 150, 150)}
        self.cursor = None

    def get_pos(self):
        pos = pm.get_pos()
        state = pm.get_pressed()
        #return pos, state
        return pm.get_pos()

    def draw(self, surface, cursor=None):
        pos = pm.get_pos()

        if self.cursor:
            c = self.cursor
        else:
            c = cursor

        self.cursors.curse(surface, pos, c)

        # color = self.cursors[c]
        # dr.line(surface, color, pos, (pos[0], pos[1] - 20))
        # dr.line(surface, color, pos, (pos[0], pos[1] + 20))
        # dr.line(surface, color, pos, (pos[0] - 20, pos[1]))
        # dr.line(surface, color, pos, (pos[0] + 20, pos[1]))
