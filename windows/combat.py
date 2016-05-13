import pygame
from window import Window
import gui


class CombatWindow(Window):
    def __init__(self, hero, monster):
        Window.__init__(self, pygame.Rect((200, 200), (400, 300)))

        close_bt = gui.Button(pygame.Rect(360, 10, 30, 30), pygame.Color('red'))
        close_bt.click = lambda a, b: self.close()
        self.add(close_bt)

        self.add(gui.Label((100, 50), 'Round 1: Fight!', pygame.Color('green')))
        self.add(gui.Label((50, 100), hero.character_class, pygame.Color('azure')))
        self.add(gui.Label((250, 100), monster.type, pygame.Color('red')))
