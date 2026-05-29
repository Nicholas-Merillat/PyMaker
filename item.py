from settings import *

from entity import Entity
from spritesheet import SpriteSheet

class Item(Entity):
    def __init__(self, x, y, width, height, item, tilemap, level): 
        super().__init__(x, y, width, height, tilemap, level)

        self.item = item

        self.spritesheet = SpriteSheet(pygame.image.load('content/images/cherry.png').convert_alpha(), (21,21))
        self.surface = self.spritesheet.get_sprite_surface(0)

        self.active = True
        self.can_fall = False
        self.can_collide = False
        
        self.sprite_offset = pygame.Vector2(14, -3)
        self.animation = 'idle'
        self.frame = 0
        self.draw_pos = (self.rect.x - self.width + self.sprite_offset.x, self.rect.y + self.sprite_offset.y)

    def animate(self, animation, delta):
        if self.animation != animation:
            self.animation = animation
        else:
            if animation == 'idle':
                if self.frame < 0: self.frame = 0
                self.frame += 0.08 * delta
                if self.frame > 7:
                    self.frame = 0
    
    def kill(self):
        super().kill()
        print(f'{self.item} kill')

    def update(self, delta, camera):
        if not self.level.paused:
            super().update(delta, camera)
            
            if not self.tilemap.editing:

                if self.tilemap.editing: self.active = False
                else: self.active = True

                if self.active:
                    pass

                # Animation

                self.animate(self.animation, delta)
            else:
                self.velocity = pygame.Vector2(0,0)
                self.x = self.spawn_x
                self.y = self.spawn_y
                self.frame = 0

            self.sprite_left = pygame.transform.flip(self.spritesheet.get_sprite_surface(int(self.frame)), True, False)
            self.sprite_right = self.spritesheet.get_sprite_surface(int(self.frame))

            self.surface = self.sprite_right

            self.draw_pos = (self.rect.x - self.width + self.sprite_offset.x, self.rect.y + self.sprite_offset.y)

    def draw(self, viewport):
        viewport.blit(self.surface, self.draw_pos)