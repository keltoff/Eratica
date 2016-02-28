from widget import widget
import pygame.draw


class Button(widget):
    def __init__(self, area, color):
        widget.__init__(self, area)
        self.color = color
        self.cursor = 'hand'

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.area, 2)
