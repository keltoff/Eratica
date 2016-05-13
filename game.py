import pygame
import pygame.locals
from pygame.rect import Rect

import sprite_loader as sl
from gui import *
from mouse import Mouse

import gui.overlay as overlay
from auxiliary import Pt

import windows as win


if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    sl.sprite_dir = 'C:\Users\M\Desktop\graphics'
    cursors = sl.load('cursors.xml')
    mouse = Mouse(display, cursors)

    gui = Gui()
    draw_stack = win.WinStack(gui)

    # gui.add(Button(Rect(710, 50, 70, 40), (255, 200, 0)))
    # gui.add(Button(Rect(710, 110, 70, 40), (255, 200, 0)))
    # gui.add(Button(Rect(600, 560, 150, 35), (255, 200, 0)))

    win_bt = Button(Rect(600, 560, 150, 35), pygame.Color('green'))
    win_bt.click = lambda a, b: draw_stack.open(win.TestWindow((100, 100)))
    gui.add(win_bt)

    # overlays = pygame.sprite.RenderUpdates()
    # pygame.display.flip()

    spriteset = sl.load('sprite_tiles.xml')

    world = Map(Rect(0, 0, 600, 550))
    world.load('mapdata.xml')
    world.sprites = spriteset
    world.start_fight = lambda h, m: draw_stack.open(win.CombatWindow(h, m))
    gui.add(world)

    sidebar = StatsBar(Rect(620, 20, 150, 300), spriteset)
    world.tile_selected = sidebar.display
    gui.add(sidebar)

    game_over = False
    while not game_over:
        world.update()

        current_gui = draw_stack.top
        c = current_gui.get_cursor_at(mouse.get_pos())

        # XXX draw all the objects here
        display.fill((0, 0, 0))
        current_gui.draw(display)
        mouse.draw(display, c)

        # overlays = pygame.sprite.RenderUpdates()
        # overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            current_gui.process_event(event)
