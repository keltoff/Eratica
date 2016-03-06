import pygame
import xml.etree.ElementTree as et
from itertools import product
from ast import literal_eval as make_tuple
from gui.widget import widget
import pygame.font
import coords

class map(widget):
    def __init__(self, area):
        widget.__init__(self, area)
        self.data = None
        self.terrain = None
        self.tile_size = 40
        self.origin = coords.Coord(150, 20)
        self.frame_color = (255, 200, 150)
        self.selected_tile = None

        pygame.font.init()
        self.font = pygame.font.SysFont('default', 50)

    def load(self, filename):
        data = et.parse(filename)
        self.data = [s.strip() for s in data.find('data').text.split()]

        self.terrain = dict()
        for ter in data.findall('terrain'):
            att = ter.attrib
            self.terrain[att['key']] = TerrainType(att)

    def draw(self, surface):
        tile = pygame.Rect(0, 0, self.tile_size, self.tile_size).move(-self.origin)
        if self.data:
            for y, x in product(range(len(self.data)), range(len(self.data[0]))):
                ter = self.terrain[self.data[y][x]]
                target = tile.move(x * self.tile_size, y * self.tile_size).clip(self.area)
                if target.width > 0:
                    pygame.draw.rect(surface, ter['color'], target)
        pygame.draw.rect(surface, self.frame_color, self.area, 2)

        if self.selected_tile:
            textpos = self.area.topleft
            surface.blit(self.font.render('{}'.format(self.selected_tile), True, (0, 200, 0)), textpos)

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
        self.stats['color'] = make_tuple(attributes['color'])

    def __getitem__(self, item):
        return self.stats[item]