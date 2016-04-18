import pygame
import pygame.locals
from pygame.rect import Rect

import sprite_loader as sl
from gui import *
from mouse import Mouse

if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    sl.sprite_dir = 'C:\Users\M\Desktop\graphics'
    cursors = sl.load('cursors.xml')
    mouse = Mouse(display, cursors)

    gui = Gui()
    # gui.add(Button(Rect(710, 50, 70, 40), (255, 200, 0)))
    # gui.add(Button(Rect(710, 110, 70, 40), (255, 200, 0)))
    # gui.add(Button(Rect(600, 560, 150, 35), (255, 200, 0)))

    # overlays = pygame.sprite.RenderUpdates()
    # pygame.display.flip()

    spriteset = sl.load('sprite_tiles.xml')

    world = Map(Rect(0, 0, 600, 550))
    world.load('mapdata.xml')
    world.sprites = spriteset
    gui.add(world)

    sidebar = StatsBar(Rect(620, 20, 150, 300), spriteset)
    world.tile_selected = sidebar.display
    gui.add(sidebar)

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
