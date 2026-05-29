from settings import *

from player import Player

class Camera():
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.dx = x + VIEWPORT_RESOLUTION[0]
        self.dy = y + VIEWPORT_RESOLUTION[1]
        self.smooth_position = True

        self.level = level

        self.smoothing_speed = 0.3
        self.limit_left = 0
        self.limit_top = 0
        self.limit_right = TILEMAP_SIZE[0] * TILE_SIZE
        self.limit_bottom = TILEMAP_SIZE[1] * TILE_SIZE

    def update(self, delta, entity):
        if not self.level.paused:
            entity_pos = pygame.Vector2(entity.x + entity.width * 0.5, entity.y + entity.height * 0.5)

            if self.smooth_position:
                self.x = pygame.math.lerp(self.x, entity_pos.x - VIEWPORT_RESOLUTION[0] * 0.5, easeInQuad(self.smoothing_speed) * delta)
                self.y = pygame.math.lerp(self.y, (entity_pos.y - VIEWPORT_RESOLUTION[1] * 0.5) - 50, easeInQuad(self.smoothing_speed) * delta)
            else:
                self.x = entity_pos.x - VIEWPORT_RESOLUTION[0] * 0.5
                self.y = (entity_pos.y - VIEWPORT_RESOLUTION[1] * 0.5) - 50

            self.dx = self.x + VIEWPORT_RESOLUTION[0]
            self.dy = self.y + VIEWPORT_RESOLUTION[1]

            if self.x < self.limit_left:
                self.x = self.limit_left
            if self.y < self.limit_top:
                self.y = self.limit_top
            if self.dx > self.limit_right:
                self.x = self.limit_right - VIEWPORT_RESOLUTION[0]
            if self.dy > self.limit_bottom:
                self.y = self.limit_bottom - VIEWPORT_RESOLUTION[1]