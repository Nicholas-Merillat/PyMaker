from settings import *

class TileSet():
    def __init__(self, name, surface):
        self.name = name
        self.surface = surface

        self.size = (int(self.surface.size[0] / TILE_SIZE), int(self.surface.size[1] / TILE_SIZE))

        # Stores the tiles in a dictionary with an ID corresponding to a tile coordinate in the tileset
        # Very inspired by how Godot does it
        self.positions = {}
        x = 0
        y = 0
        for i in range(self.size[0] * self.size[1]):
            x = i % self.size[0]

            self.positions.update({str(i):(x,y)})

            if (x + 1) / self.size[0] >= 1:
                y += 1

    def get_tile_surface(self, tile_index):
        surface = self.surface.subsurface((self.positions[str(tile_index)][0] * TILE_SIZE, self.positions[str(tile_index)][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return surface