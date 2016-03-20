__author__ = 'tryid_000'

import pygame
import pygame.locals

import map as mm
from mouse import Mouse
from gui.gui import Gui
from gui.button import Button
from pygame.rect import Rect
import sprite_loader as sl

if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    sl.sprite_dir = 'C:\Users\M\Desktop\graphics'
    cursors = sl.load('cursors.xml')
    mouse = Mouse(display, cursors)

    gui = Gui()
    gui.add(Button(Rect(710, 50, 70, 40), (255, 200, 0)))
    gui.add(Button(Rect(710, 110, 70, 40), (255, 200, 0)))
    gui.add(Button(Rect(600, 560, 150, 35), (255, 200, 0)))

    # overlays = pygame.sprite.RenderUpdates()
    # pygame.display.flip()

    spriteset = sl.load('sprite_tiles.xml')

    world = mm.Map(Rect(0, 0, 700, 550))
    world.load('mapdata.xml')
    world.sprites = spriteset
    gui.add(world)

    game_over = False
    while not game_over:
        world.update()

        c = gui.get_cursor_at(mouse.get_pos())

        # XXX draw all the objects here
        display.fill((0, 0, 0))
        gui.draw(display)
        mouse.draw(display, c)

        # overlays = pygame.sprite.RenderUpdates()
        # overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            gui.process_event(event)
