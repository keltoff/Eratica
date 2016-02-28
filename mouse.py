import pygame.mouse as pm
import pygame.image as im

class Mouse:
    def __init__(self, surface):
        pm.set_visible(False)
        self.cursor = im.load("graphics/Cursor_GreyLight.png").convert_alpha(surface)

    def get_pos(self):
        pos = pm.get_pos()
        state = pm.get_pressed()
        return pos, state

    def draw(self, surface):
        pos = pm.get_pos()
        surface.blit(self.cursor, pos)
