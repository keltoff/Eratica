import widget
import pygame.draw
import text_helper



class StatsBar(widget.Widget):
    def __init__(self, area, sprites):
        widget.Widget.__init__(self, area)
        self.sprites = sprites
        self.data = None
        self.color = (50, 50, 50)

    def draw(self, surface):
        widget_surf = surface.subsurface(self.area)
        pygame.draw.rect(widget_surf, self.color, widget_surf.get_rect(), 2)

        if self.data:
            if 'terrain' in self.data and self.data['terrain']:
                terrain = self.data['terrain']
                self.sprites.blit(widget_surf, (35, 35), terrain['sprite'])
                text_helper.draw_text(widget_surf, terrain['name'], (60, 25), (200, 200, 200))
            if 'places' in self.data:
                text_helper.draw_text(widget_surf, 'Places: {}'.format(len(self.data['places'])), (20, 80), (200, 200, 200))
            if 'monsters' in self.data:
                text_helper.draw_text(widget_surf, 'Monsters: {}'.format(len(self.data['monsters'])), (20, 120), (200, 200, 200))

    def display(self, data):
        self.data = data
