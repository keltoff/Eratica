import pygame
import pygame.locals as pl
import xml.etree.ElementTree as et
from itertools import product
from ast import literal_eval as evaluate
from gui.widget import widget
import pygame.font
from coords import Pt
from safedict import SafeDict
from text_helper import draw_text


class Map(widget):
    def __init__(self, area):
        widget.__init__(self, area)
        self.data = None
        self.terrain = None
        self.tile_size = 32
        self.origin = Pt(0, 0)
        self.frame_color = (255, 200, 150)
        self.selected_tile = None
        self.scroll_speed = Pt(0, 0)
        self.keydir = __build_keydir__()

        self.places = None
        self.monsters = None

        self.sprites = None
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
        surface.fill((0, 0, 0), self.area)
        self.draw_map(surface.subsurface(self.area))
        pygame.draw.rect(surface, self.frame_color, self.area, 2)

    def draw_map(self, surface):
        tile = pygame.Rect(0, 0, self.tile_size, self.tile_size)

        def current_view(X):
            return X * self.tile_size - self.origin

        if self.data:
            for y, x in product(range(len(self.data)), range(len(self.data[0]))):
                ter = self.terrain[self.data[y][x]]
                target = tile.move(current_view(Pt(x, y)))
                if target.width > 0:
                    # pygame.draw.rect(surface, ter['color'], target)
                    subkey = self.neighborhood(x, y, ter)
                    self.sprites.blit(surface, target, ter['sprite'], subkey)

        for c in self.places:
            self.sprites.blit(surface, tile.move(current_view(c.pos)), c.key)

        for m in self.monsters:
            self.sprites.blit(surface, tile.move(current_view(m.pos)), m.type)

        if self.selected_tile:
            draw_text(surface, '{}'.format(self.selected_tile), self.area.topleft, (0, 200, 0))
            pygame.draw.rect(surface, (200, 200, 50), tile.move(current_view(self.selected_tile)), 1)

    def neighborhood(self, x, y, ter):
        if not ter.borders:
            return None

        subkey = '{:0}{:0}{:0}{:0}'.format(
            self.is_different(x, y-1, ter),
            self.is_different(x+1, y, ter),
            self.is_different(x, y+1, ter),
            self.is_different(x-1, y, ter))

        if (ter.corners and
            (subkey == '1100' and self.is_different(x-1, y+1, ter)) or
            (subkey == '0110' and self.is_different(x-1, y-1, ter)) or
            (subkey == '0011' and self.is_different(x+1, y-1, ter)) or
            (subkey == '1001' and self.is_different(x+1, y+1, ter))):
                subkey = 'c' + subkey

        return subkey

    def is_different(self, x, y, ter):
        if 0 <= y < len(self.data) and 0 <= x < len(self.data[y]):
            return self.data[y][x] != ter['key']
        else:
            return False

    def update(self):
        self.origin += self.scroll_speed * 3

        if self.origin.x < 0:
            self.origin = Pt(0, self.origin.y)

        if self.origin.y < 0:
            self.origin = Pt(self.origin.x, 0)

    def get_cursor(self, pos):
        if self.tile_at(pos)[0]:
            return 'frame'
        else:
            return None

    def tile_at(self, pos):
        tilepos = (pos + self.origin) / self.tile_size
        x, y = tilepos
        if len(self.data) > y and len(self.data[y]) > x:
            return tilepos, self.data[y][x]
        else:
            return None, None

    # event handling
    def process_event(self, event):
        if event.type == pl.KEYDOWN:
            # fast = event.mod
            self.scroll_speed += self.keydir[event.key]
        if event.type == pl.KEYUP:
            self.scroll_speed -= self.keydir[event.key]

    def click(self, pos, button):
        pass

    def mouse_move(self, pos):
        self.selected_tile, _ = self.tile_at(pos)


def __build_keydir__():
    keydir = SafeDict()
    keydir[pl.K_UP] = Pt(0, -1)
    keydir[pl.K_DOWN] = Pt(0, 1)
    keydir[pl.K_LEFT] = Pt(-1, 0)
    keydir[pl.K_RIGHT] = Pt(1, 0)
    keydir.default = Pt(0, 0)
    return keydir


class TerrainType:
    def __init__(self, attributes):
        self.stats = attributes
        self.stats['color'] = evaluate(attributes['color'])

    def __getitem__(self, item):
        return self.stats[item]

    @property
    def borders(self):
        return self.stats.get('borders', False)

    @property
    def corners(self):
        return self.stats.get('corners', False)


class Monster:
    def __init__(self, data):
        self.pos = Pt(evaluate(data['pos']))
        self.type = data['type']
        self.color = evaluate(data['color'])

    def draw(self, surface, pos_correction):
        target = pos_correction(self.pos)
        draw_text(surface, self.type, target, self.color)


class Cave:
    def __init__(self, data):
        self.pos = Pt(evaluate(data['pos']))
        self.key = data['key']
        self.color = evaluate(data['color'])

    def draw(self, surface, pos_correction):
        target = pos_correction(self.pos)
        draw_text(surface, self.key, target, self.color)
