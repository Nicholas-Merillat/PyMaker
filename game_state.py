from settings import *

class GameState():
    def __init__(self, name, main):
        self.name = name
        self.main = main

    def load(self):
        print(f'{self.name} is loaded')
    def input(self):
        raise NotImplementedError('Do not use GameState on its own!')
    def run(self):
        raise NotImplementedError('Do not use GameState on its own!')
    def draw(self):
        raise NotImplementedError('Do not use GameState on its own!')
    def refresh(self):
        raise NotImplementedError('Do not use GameState on its own!')
    def exit(self):
        raise NotImplementedError('Do not use GameState on its own!')