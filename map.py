import pygame
import xml.etree.ElementTree as et
from itertools import product
from ast import literal_eval as make_tuple

class map:
    def __init__(self, size):
        self.area = pygame.Rect(size)
        self.data = None
        self.terrain = None
        self.tile_size = 60

    def load(self, file):
        data = et.parse(file)
        self.data = [s.strip() for s in data.find('data').text.split()]

        self.terrain = dict()
        for ter in data.findall('terrain'):
            att = ter.attrib
            self.terrain[att['key']] = TerrainType(att)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 200, 150), self.area, 2)

        for x, y in product(range(self.area.width / self.tile_size), range(self.area.height / self.tile_size)):
            ter = self.terrain[self.data[y][x]]
            pygame.draw.rect(surface, ter['color'], pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))


class TerrainType:
    def __init__(self, attributes):
        self.stats = attributes
        self.stats['color'] = make_tuple(attributes['color'])

    def __getitem__(self, item):
        return self.stats[item]