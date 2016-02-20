import pygame

class map:
    def __init__(self, size):
        self.size = size
        self.data = None

    def load(self, file):
        self.data = file