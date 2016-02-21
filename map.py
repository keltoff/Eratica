import pygame
import xml.etree.ElementTree as et
from itertools import product
from ast import literal_eval as make_tuple

class map:
    def __init__(self, size):
        self.area = pygame.Rect(size)
        self.data = None
        self.terrain = None
        self.tile_size = 40
        self.origin = (150, 20)
        self.frame_color = (255, 200, 150)

    def load(self, file):
        data = et.parse(file)
        self.data = [s.strip() for s in data.find('data').text.split()]

        self.terrain = dict()
        for ter in data.findall('terrain'):
            att = ter.attrib
            self.terrain[att['key']] = TerrainType(att)

    def draw(self, surface):
        tile = pygame.Rect(0, 0, self.tile_size, self.tile_size).move(-self.origin[0], -self.origin[1])
        if self.data:
            for y, x in product(range(len(self.data)), range(len(self.data[0]))):
                ter = self.terrain[self.data[y][x]]
                target = tile.move(x * self.tile_size, y * self.tile_size).clip(self.area)
                if target.width > 0:
                    pygame.draw.rect(surface, ter['color'], target)
        pygame.draw.rect(surface, self.frame_color, self.area, 2)


class TerrainType:
    def __init__(self, attributes):
        self.stats = attributes
        self.stats['color'] = make_tuple(attributes['color'])

    def __getitem__(self, item):
        return self.stats[item]