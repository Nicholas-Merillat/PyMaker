from settings import *

# Basically just tileset but for spritesheets

class SpriteSheet():
    def __init__(self, surface, sprite_size):
        self.surface = surface
        self.sprite_size = sprite_size

        self.size = (int(self.surface.size[0] / self.sprite_size[0]), int(self.surface.size[1] / self.sprite_size[1]))

        self.positions = {}
        x = 0
        y = 0
        for i in range(self.size[0] * self.size[1]):
            x = i % self.size[0]

            self.positions.update({str(i):(x,y)})

            if (x + 1) / self.size[0] >= 1:
                y += 1

    def get_sprite_surface(self, sprite_index):
        surface = self.surface.subsurface((self.positions[str(sprite_index)][0] * self.sprite_size[0], self.positions[str(sprite_index)][1] * self.sprite_size[1], self.sprite_size[0], self.sprite_size[1]))
        return surface