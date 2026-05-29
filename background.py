from settings import *

class Background():
    def __init__(self):
        self.sky = pygame.image.load('content/images/background-sky.png').convert()
        self.trees = pygame.image.load('content/images/background-trees.png').convert_alpha()
        self.mountains = pygame.image.load('content/images/background-mountains.png').convert_alpha()
        self.far_mountains = pygame.image.load('content/images/background-far-mountains.png').convert_alpha()

        self.sky = pygame.transform.scale(self.sky, (self.sky.size[0] * 2, self.sky.size[1] * 2))
        self.trees = pygame.transform.scale(self.trees, (self.trees.size[0] * 3, self.trees.size[1] * 3))
        self.mountains = pygame.transform.scale(self.mountains, (self.mountains.size[0] * 2, self.mountains.size[1] * 2))
        self.far_mountains = pygame.transform.scale(self.far_mountains, (self.far_mountains.size[0] * 4, self.far_mountains.size[1] * 4))

        self.surface = pygame.Surface((VIEWPORT_RESOLUTION[0], VIEWPORT_RESOLUTION[1] / 0.75)).convert()

    def update(self, camera):
        self.surface.blit(self.sky, pygame.Vector2(0,0))

        self.surface.blit(self.far_mountains, pygame.Vector2((0 - camera.x / 8) % -self.far_mountains.width, -250 - camera.y / 8))
        self.surface.blit(self.far_mountains, pygame.Vector2(((0 + self.far_mountains.width) - camera.x / 8) % self.far_mountains.width, -250 - camera.y / 8))

        self.surface.blit(self.mountains, pygame.Vector2((0 - camera.x / 6) % -self.mountains.width, 0 - camera.y / 6))
        self.surface.blit(self.mountains, pygame.Vector2(((0 + self.mountains.width) - camera.x / 6) % self.mountains.width, 0 - camera.y / 6))

        self.surface.blit(self.trees, pygame.Vector2((0 - camera.x / 4) % -self.trees.width, -150 - (camera.y / 4) + 100))
        self.surface.blit(self.trees, pygame.Vector2(((0 + self.trees.width) - camera.x / 4) % self.trees.width, -150 - (camera.y / 4) + 100))