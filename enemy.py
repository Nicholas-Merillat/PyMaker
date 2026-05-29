from settings import *

from entity import Entity
from spritesheet import SpriteSheet

class Enemy(Entity):
    def __init__(self, x, y, width, height, enemy, tilemap, level): 
        super().__init__(x, y, width, height, tilemap, level)

        self.enemy = enemy

        self.spritesheet = SpriteSheet(pygame.image.load('content/images/opossum.png').convert_alpha(), (36,28))
        self.surface = self.spritesheet.get_sprite_surface(0)

        self.can_wall_jump = False
        self.active = True
        self.direction = 1

        self.speed_accel = 0.04
        self.speed_max = 1
        self.gravity = 0.15
        self.fall_speed_cap = 5
        self.jump_force = -3.75
        
        self.sprite_offset = pygame.Vector2(2, -18)
        self.animation = 'idle'
        self.frame = 0
        self.draw_pos = (self.rect.x - self.width + self.sprite_offset.x, self.rect.y + self.sprite_offset.y)

    def animate(self, animation, delta):
        if self.animation != animation:
            self.animation = animation
        else:
            if animation == 'idle':
                self.frame = 0
            elif animation == 'walk':
                if self.frame < 0: self.frame = 0
                if self.velocity.x > 0:
                    self.frame += numpy.interp(self.velocity.x, [0, self.speed_max], [0.05, 0.175]) * delta
                elif self.velocity.x < 0:
                    self.frame += numpy.interp(self.velocity.x, [-self.speed_max, 0], [0.175, 0.05]) * delta
                if self.frame > 6:
                    self.frame = 0

    def kill(self):
        super().kill()
        print(f'{self.enemy} kill')

    def update(self, delta, camera, player_pos):
        if not self.level.paused:
            self.wall_jumping = False

            super().update(delta, camera)
            
            if not self.tilemap.editing:

                if self.tilemap.editing: self.active = False
                else: self.active = True

                if self.active:
                    if self.enemy == 'opossum':
                        if self.is_on_ground:
                            self.below_tile_left = self.tilemap.world_to_tile(self.x, self.dy)
                            self.below_tile_right = self.tilemap.world_to_tile(self.dx, self.dy)
                            if self.tilemap.grid[int(self.below_tile_left.x)][int(self.below_tile_left.y)] == 0:
                                self.direction = 1
                            elif self.tilemap.grid[int(self.below_tile_right.x)][int(self.below_tile_right.y)] == 0:
                                self.direction = -1

                            if self.is_on_wall:
                                self.direction /= -1

                            if self.x == 0:
                                self.direction = 1
                            elif int(self.dx) == (TILEMAP_SIZE[0] * TILE_SIZE):
                                self.direction = -1

                # Animation

                if not self.is_on_ground:
                    if self.velocity.y > 0:
                        if self.wall_jumping:
                            self.animation = 'wall_jump'
                        else:
                            self.animation = 'fall'
                    else:
                        self.animation = 'jump'
                else:
                    if self.crouching:
                        self.animation = 'crouch'
                    elif self.looking_up:
                        self.animation = 'look_up'
                    else:
                        if (self.velocity.x > 0.15 or self.velocity.x < -0.15) or (self.direction != 0 and not self.is_on_wall):
                            self.animation = 'walk'
                        else:
                            self.animation = 'idle'

                self.animate(self.animation, delta)
            else:
                self.velocity = pygame.Vector2(0,0)
                self.x = self.spawn_x
                self.y = self.spawn_y
                self.last_direction = 1
                self.direction = 1
                self.frame = 2

            self.sprite_left = pygame.transform.flip(self.spritesheet.get_sprite_surface(int(self.frame)), True, False)
            self.sprite_right = self.spritesheet.get_sprite_surface(int(self.frame))

            if self.last_direction < 0:
                self.surface = self.sprite_right
                self.sprite_offset = pygame.Vector2(15, -14)
            elif self.last_direction > 0:
                self.surface = self.sprite_left
                self.sprite_offset = pygame.Vector2(9, -14)

            self.draw_pos = (self.rect.x - self.width + self.sprite_offset.x, self.rect.y + self.sprite_offset.y)

    def draw(self, viewport):
        viewport.blit(self.surface, self.draw_pos)