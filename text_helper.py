import pygame.font

pygame.font.init()
textfont = pygame.font.SysFont('default', 50)

def draw_text(surface, text, pos, color=(0, 200, 0)):
    surface.blit(textfont.render(text, True, color), pos)
