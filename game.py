__author__ = 'tryid_000'

import pygame
import pygame.locals

import map as mm

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((640, 480))

    clock = pygame.time.Clock()

    # overlays = pygame.sprite.RenderUpdates()
    # pygame.display.flip()

    world = mm.map((0, 0, 400, 400))
    world.load('mapdata.txt')

    game_over = False
    while not game_over:

        # XXX draw all the objects here
        world.draw()

        # overlays = pygame.sprite.RenderUpdates()
        # overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                pass
            elif event.type == pygame.locals.KEYUP:
                pass