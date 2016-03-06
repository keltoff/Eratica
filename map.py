import pygame
import xml.etree.ElementTree as et
from itertools import product
from ast import literal_eval as evaluate
from gui.widget import widget
import pygame.font
import coords

pygame.font.init()
textfont = pygame.font.SysFont('default', 50)


def __textout__(surface, text, pos, color=(0, 200, 0)):
    surface.blit(textfont.render(text, True, color), pos)


class Map(widget):
    def __init__(self, area):
        widget.__init__(self, area)
        self.data = None
        self.terrain = None
        self.tile_size = 40
        self.origin = coords.Coord(150, 20)
        self.frame_color = (255, 200, 150)
        self.selected_tile = None

        self.places = None
        self.monsters = None

        self.font = pygame.font.SysFont('default', 50)

    def load(self, filename):
        data = et.parse(filename)
        self.data = [s.strip() for s in data.find('data').text.split()]

        self.terrain = dict()
        for ter in data.findall('terrain'):
            att = ter.attrib
            self.terrain[att['key']] = TerrainType(att)

        self.monsters = [Monster(m.attrib) for m in data.findall('.//places/monster')]
        self.places = [Cave(c.attrib) for c in data.findall('.//places/cave')]

    def draw(self, surface):
        tile = pygame.Rect(0, 0, self.tile_size, self.tile_size)

        def current_view(X):
            return X * self.tile_size - self.origin

        if self.data:
            for y, x in product(range(len(self.data)), range(len(self.data[0]))):
                ter = self.terrain[self.data[y][x]]
                target = tile.move(current_view(coords.Coord(x, y))).clip(self.area)
                if target.width > 0:
                    pygame.draw.rect(surface, ter['color'], target)
        pygame.draw.rect(surface, self.frame_color, self.area, 2)

        for c in self.places:
            c.draw(surface, current_view)

        for m in self.monsters:
            m.draw(surface, current_view)

        if self.selected_tile:
            textpos = self.area.topleft
            surface.blit(self.font.render('{}'.format(self.selected_tile), True, (0, 200, 0)), textpos)
            pygame.draw.rect(surface, (0, 100, 200), tile.move(current_view(self.selected_tile)), 1)

    def get_cursor(self, pos):
        self.selected_tile, _ = self.tile_at(pos)
        if self.selected_tile:
            return 'frame'
        else:
            return None

    def process_event(self, event):
        pass

    def tile_at(self, pos):
        tilepos = (pos + self.origin) / self.tile_size
        x, y = tilepos
        if len(self.data) > y and len(self.data[y]) > x:
            return tilepos, self.data[y][x]
        else:
            return None, None


class TerrainType:
    def __init__(self, attributes):
        self.stats = attributes
        self.stats['color'] = evaluate(attributes['color'])

    def __getitem__(self, item):
        return self.stats[item]


class Monster:
    def __init__(self, data):
        self.pos = coords.Coord(evaluate(data['pos']))
        self.type = data['type']
        self.color = evaluate(data['color'])

    def draw(self, surface, pos_correction):
        target = pos_correction(self.pos)
        __textout__(surface, self.type, target, self.color)


class Cave:
    def __init__(self, data):
        self.pos = coords.Coord(evaluate(data['pos']))
        self.key = data['key']
        self.color = evaluate(data['color'])

    def draw(self, surface, pos_correction):
        target = pos_correction(self.pos)
        __textout__(surface, self.key, target, self.color)
