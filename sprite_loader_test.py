import sprite_loader as sl

import pygame
import pygame.locals
import pygame.draw
from pygame.rect import Rect


sl.sprite_dir = 'C:\Users\M\Desktop\graphics'

sprite_set = sl.load('spritedata.xml')

# sl.save(sprite_set, 'save_test.xml', 'blah.png')

pygame.init()
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

sprite_set.convert(display)

game_over = False
while not game_over:
    display.fill((0, 0, 0))

    #draw whatever
    #sprite_set.test_draw(display)
    sprite_set.blit(display, (100, 100), 'red', 'chibi')
    sprite_set.blit(display, (200, 100), 'red', 'mid')
    sprite_set.blit(display, (300, 100), 'red', 2)

    sprite_set.blit(display, (300, 200), 'green', 1)
    pygame.draw.line(display, (255, 0, 0), (250, 200), (350, 200))
    pygame.draw.line(display, (255, 0, 0), (300, 150), (300, 250))

    rect = pygame.Rect(100, 200, 100, 100)
    sprite_set.blit(display, rect, 'green', 0)
    pygame.draw.rect(display, (255, 0, 0), rect, 1)

    pygame.display.flip()
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            game_over = True
