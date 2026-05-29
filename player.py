from settings import *

from entity import Entity
from spritesheet import SpriteSheet

class Player(Entity):
    def __init__(self, x, y, width, height, tilemap, level): 
        super().__init__(x, y, width, height, tilemap, level)

        self.spritesheet = SpriteSheet(pygame.image.load('content/images/player.png').convert_alpha(), (33,32))
        self.surface = self.spritesheet.get_sprite_surface(15)

        self.bounding_rect = pygame.Rect(0,0, width+10, height+10)

        self.speed_accel = 0.04
        self.speed_max = 1.5
        self.gravity = 0.15
        self.fall_speed_cap = 5
        self.jump_force = -4.5
        self.knockback_force = 4

        self.can_collide_end = False
        self.can_wall_jump = True
        self.stunned = False
        self.cherries = 0
        self.lives = 3
        self.health = 3

        self.sprite_offset = pygame.Vector2(2, -18)
        self.animation = 'idle'
        self.frame = 0
        self.draw_pos = (self.rect.x - self.width + self.sprite_offset.x, self.rect.y + self.sprite_offset.y)

    def animate(self, animation, delta):
        if self.animation != animation:
            self.animation = animation
        else:
            if animation == 'idle':
                if self.frame < 15: self.frame = 15
                self.frame += 0.065 * delta
                if self.frame > 19:
                    self.frame = 15
            elif animation == 'walk':
                if self.frame < 21: self.frame = 21
                if self.velocity.x > 0:
                    self.frame += numpy.interp(self.velocity.x, [0, self.speed_max], [0.05, 0.2]) * delta
                elif self.velocity.x < 0:
                    self.frame += numpy.interp(self.velocity.x, [-self.speed_max, 0], [0.2, 0.05]) * delta
                if self.frame > 27:
                    self.frame = 21
            elif animation == 'jump':
                self.frame = 19
            elif animation == 'fall':
                self.frame = 20
            elif animation == 'crouch':
                if self.frame < 11:
                    self.frame = 11
                self.frame += 0.05 * delta
                if self.frame > 13:
                    self.frame = 11
            elif animation == 'look_up':
                self.frame = 7
            elif self.animation == 'wall_jump':
                self.frame = 33

    def kill(self):
        print('player kill')
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.velocity = pygame.Vector2(0,0)
        self.cherries = 0
        self.lives -= 1
        self.health = 3

    def update(self, delta, camera, keys):
        if not self.level.paused:
            self.wall_jumping = False
            if not self.tilemap.editing:
                if not self.stunned: self.direction = -int(keys[pygame.K_LEFT]) + int(keys[pygame.K_RIGHT])
                else: self.direction = 0

                self.want_to_jump = keys[pygame.K_z]
                self.crouching = keys[pygame.K_DOWN] and self.is_on_ground
                self.looking_up = keys[pygame.K_UP] and self.is_on_ground

                super().update(delta, camera)

                if self.velocity.y > 0 or self.is_on_ground:
                    self.stunned = False

                # Kinda inefficient if there's lots of enemies but oh well i only have until tomorrow morning
                for enemy in self.tilemap.enemies:
                    if enemy.alive and self.rect.colliderect(enemy.rect):
                        if self.dy <= enemy.y + enemy.height * 0.5 and self.velocity.y > 0:
                            enemy.kill()
                            self.stunned = False
                            if self.want_to_jump:
                                self.velocity.y = self.jump_force
                            else:
                                self.jumping = False
                                self.velocity.y = self.jump_force * 0.5
                        elif not self.stunned:
                            self.health -= 1
                            if self.x + self.width * 0.5 > enemy.x + enemy.width * 0.5:
                                self.last_direction = -1
                            else:
                                self.last_direction = 1
                            self.stunned = True
                            self.velocity.x = self.knockback_force * (self.last_direction / -1)
                            self.velocity.y = self.jump_force * 0.25
                
                for item in self.tilemap.items:
                    if item.alive and self.bounding_rect.colliderect(item.rect):
                        item.kill()
                        self.cherries += 1
                
                if self.stunned:
                    if self.velocity.x > self.knockback_force:
                        self.velocity.x = self.knockback_force
                    elif self.velocity.x < self.knockback_force / -1:
                        self.velocity.x = self.knockback_force / -1

                if self.dx > self.limit_right:
                    pass

                if self.health <= 0:
                    self.kill()

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
                self.want_to_jump = False
                self.crouching = False
                self.looking_up = False
                self.jumping = False
                self.cherries = 0
                self.health = 3

                self.direction = pygame.Vector2(-int(keys[pygame.K_a]) + int(keys[pygame.K_d]), -int(keys[pygame.K_w]) + int(keys[pygame.K_s]))
                if self.direction.x != 0 and self.direction.y != 0: self.direction.normalize_ip()
                if self.direction.x != 0: self.last_direction = self.direction.x

                self.velocity = pygame.Vector2(self.direction.x * self.speed_max * 2, self.direction.y * self.speed_max * 2)

                self.x += self.velocity.x * delta
                self.y += self.velocity.y * delta
                self.rect.x = self.x - camera.x
                self.rect.y = self.y - camera.y

                self.frame = 15

            # Run whether or not editing    

            self.bounding_rect.x = self.rect.x - 5
            self.bounding_rect.y = self.rect.y - 10

            self.sprite_left = pygame.transform.flip(self.spritesheet.get_sprite_surface(int(self.frame)), True, False)
            self.sprite_right = self.spritesheet.get_sprite_surface(int(self.frame))

            if self.last_direction < 0:
                self.surface = self.sprite_left
                self.sprite_offset = pygame.Vector2(1, -18)
            elif self.last_direction > 0:
                self.surface = self.sprite_right
                self.sprite_offset = pygame.Vector2(2, -18)

            self.draw_pos = (self.rect.x - self.width + self.sprite_offset.x, self.rect.y + self.sprite_offset.y)

    def draw(self, viewport):
        viewport.blit(self.surface, self.draw_pos)