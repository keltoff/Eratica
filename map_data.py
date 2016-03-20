import xml.etree.ElementTree as et
from auxiliary import Pt
from ast import literal_eval as evaluate
from itertools import product


class MapData():
    def __init__(self):
        self.data = None
        self.terrain = None

        self.selected_tile = None

        self.places = None
        self.monsters = None

    def __getitem__(self, item):
        if item.__class__ == tuple:
            x, y = item
            if len(self.data) > y and len(self.data[y]) > x:
                return self.data[y][x]
        else:
            return None, None

    def __iter__(self):
        for y, x in product(range(len(self.data)), range(len(self.data[0]))):
            ter = self.terrain[self.data[y][x]]
            yield x, y, ter

    def load(self, filename):
        data = et.parse(filename)
        self.data = [s.strip() for s in data.find('data').text.split()]

        self.terrain = dict()
        for ter in data.findall('terrain'):
            att = ter.attrib
            self.terrain[att['key']] = TerrainType(att)

        self.monsters = [Monster(m.attrib) for m in data.findall('.//places/monster')]
        self.places = [Cave(c.attrib) for c in data.findall('.//places/cave')]

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


class Cave:
    def __init__(self, data):
        self.pos = Pt(evaluate(data['pos']))
        self.key = data['key']
        self.color = evaluate(data['color'])

    def draw(self, surface, pos_correction):
        target = pos_correction(self.pos)
