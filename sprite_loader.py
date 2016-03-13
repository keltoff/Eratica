import xml.etree.ElementTree as et
import os.path as path
from ast import literal_eval as evaluate
import pygame
from coords import Pt


sprite_dir = '.'


def load(filename):
    root = et.parse(filename)

    gdata = root.find('./graphics').attrib
    img_file = path.join(sprite_dir, gdata['file'])
    transparent = gdata.get('transparent', False)

    graphic = pygame.image.load(img_file)
    if transparent:
        if transparent in ['default', 'yes', 'True']:
            transparent = True
        elif transparent in ['no', 'False', 'None']:
            transparent = False
        else:
            graphic.set_colorkey(evaluate(transparent))
            transparent = 'key'

    sprites = dict()
    for snode in root.findall('./sprite'):
        sprite = dict()
        sprites[snode.attrib['key']] = sprite
        for i, frame in enumerate(snode.findall('./img')):
            sprite[i] = pygame.Rect(evaluate(frame.attrib['rect']))
            if 'key' in frame.attrib:
                sprite[frame.attrib['key']] = sprite[i]

        for alias in snode.findall('./alias'):
            sprite[alias.attrib['key']] = sprite[alias.attrib['means']]

    for alias in root.findall('./alias'):
        sprites[alias.attrib['key']] = sprites[alias.attrib['means']]

    result = SpriteSet(graphic, sprites)
    result.graphic_file = filename
    result.transparence = transparent
    return result


def save(sprite_set, filename):
    root = et.Element("set")

    transparence = '{}'.format(sprite_set.transparence)
    if transparence == 'key':
        transparence = '{}'.format(sprite_set.graphic.get_colorkey())
    et.SubElement(root, "graphics", file=sprite_set.graphic_file, transparent=transparence)

    previous = []
    for key in sprite_set.rects:
        add_sprite_node(root, key, sprite_set.rects[key], previous)

    tree = et.ElementTree(root)
    tree.write(filename)


def add_sprite_node(root, key, rect_dict, previous):
    if rect_dict in previous:
        # et.SubElement(root, 'alias', key=key, means=previous[rect_dict])
        pass
    else:
        snode = et.SubElement(root, 'sprite', key=key)
        previous.append(rect_dict)
        prev_imgs = []
        for sp_key in rect_dict:
            add_img_node(snode, sp_key, rect_dict[sp_key], prev_imgs)


def add_img_node(parent, key, rect, previous):
    if rect in previous:
        # et.SubElement(parent, 'alias', key=key, means=previous[key])
        pass
    else:
        et.SubElement(parent, 'img', rect=rect2str(rect),  key='{}'.format(key))
        previous.append(rect)


def rect2str(rect):
    return '({}, {}, {}, {})'.format(rect.left, rect.top, rect.width, rect.height)


def slice(img_file):
    img_file = path.join(sprite_dir, img_file)
    graphic = pygame.image.load(img_file)

    sprites = dict()
    # chop chop

    return SpriteSet(graphic, sprites)


class SpriteSet:
    def __init__(self, graphics, sprites):
        self.graphics = graphics
        self.rects = sprites
        self.graphic_file = None
        self.transparence = True

    def __getitem__(self, item):
        if item is tuple:
            return self.get_sprite(item[0], item[1])
        else:
            return self.get_sprite(item)

    def convert(self, target):
        self.graphics = self.graphics.convert_alpha(target)

    def get_sprite(self, key, subkey=None):
        if not subkey:
            subkey = 0

        return self.graphics.subsurface(self.rects[key][subkey])

    def blit(self, target, destination, key, subkey=None):
        sprite = self.get_sprite(key, subkey)

        if destination.__class__ == pygame.Rect:
            center_pos = Pt(destination.center) - Pt(sprite.get_size())/2
        else:
            center_pos = Pt(destination) - Pt(sprite.get_size())/2
        target.blit(sprite, center_pos)

    def test_draw(self, target):
        target.blit(self.graphics, (0, 0))

        frame_col = (250, 0, 0)
        sec_col = (0, 250, 0)
        for sprite_val in self.rects.values():
            for img_val in sprite_val.values():
                pygame.draw.rect(target, sec_col, img_val, 2)
            pygame.draw.rect(target, frame_col, sprite_val[0], 2)
