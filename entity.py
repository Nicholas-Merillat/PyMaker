from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, tilemap, level):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True

        self.x = x
        self.y = y
        self.dx = x + width
        self.dy = y + height
        self.spawn_x = x
        self.spawn_y = y
        self.width = width
        self.height = height
        self.tilemap = tilemap
        self.level = level

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255,0,0))

        self.rect = self.surface.get_rect()

        self.can_collide = True
        self.can_collide_end = True
        self.direction = 0
        self.last_direction = 1
        self.can_jump = True
        self.can_wall_jump = False
        self.can_fall = True
        self.crouching = False
        self.looking_up = False
        self.want_to_jump = False
        self.jumping = False
        self.is_on_ground = False

        self.speed_accel = 0.04
        self.speed_max = 1.5
        self.gravity = 0.15
        self.fall_speed_cap = 5
        self.jump_force = -3.75
        self.jump_cancel_factor = 0.8

        self.velocity = pygame.Vector2(0,0)
        self.limit_right = TILE_SIZE * TILEMAP_SIZE[0]
        self.limit_bottom = TILE_SIZE * TILEMAP_SIZE[1]

    def kill(self):
        self.alive = False

    def update(self, delta, camera):
        if not self.level.paused:
            if not self.tilemap.editing:
                if self.direction != 0: self.last_direction = self.direction

                if self.want_to_jump == False: self.can_jump = True

                if self.crouching or self.looking_up: self.direction = 0

                self.velocity.x = pygame.math.lerp(self.velocity.x, self.speed_max * self.direction, easeOutQuad(self.speed_accel) * delta)
                if abs(self.velocity.x) < 0.001: # Fixes weird bug with lerping to 0
                    self.velocity.x = 0

                if self.can_fall: self.velocity.y += self.gravity * delta
                if self.velocity.y > self.fall_speed_cap:
                    self.velocity.y = self.fall_speed_cap

                self.prev_x = self.x
                self.prev_y = self.y
                self.x += self.velocity.x * delta
                self.y += self.velocity.y * delta

                # MESSES UP COLLISION PRETTY BAD SOMETIMES SO DISABLED FOR NOW 

                # Prevents entity from traveling a distance greater than a singular tile (This fixes the bug with window focus and delta)
                # if abs(self.y - self.prev_y) > TILE_SIZE:
                #     self.y = self.prev_y
                # if abs(self.x - self.prev_x) > TILE_SIZE:
                #     self.x = self.prev_x

                self.dx = self.x + self.width
                self.dy = self.y + self.height

                # Get the surrounding tiles around the entity and if there are any tiles, do collision
                self.is_on_ground = False
                self.is_on_wall = False

                if self.can_collide:
                    self.below_tile_left = self.tilemap.world_to_tile(self.x + 1, self.dy)
                    self.below_tile_right = self.tilemap.world_to_tile(self.dx - 1, self.dy)
                    if self.tilemap.grid[int(self.below_tile_left.x)][int(self.below_tile_left.y)] != 0 and self.velocity.y >= 0:
                        self.y = self.below_tile_left.y * TILE_SIZE - self.height
                        self.velocity.y = 0
                        self.is_on_ground = True
                    elif self.tilemap.grid[int(self.below_tile_right.x)][int(self.below_tile_right.y)] != 0 and self.velocity.y >= 0:
                        self.y = self.below_tile_right.y * TILE_SIZE - self.height
                        self.velocity.y = 0
                        self.is_on_ground = True

                    self.above_tile_left = self.tilemap.world_to_tile(self.x + 1, self.y)
                    self.above_tile_right = self.tilemap.world_to_tile(self.dx - 1, self.y)
                    if self.tilemap.grid[int(self.above_tile_left.x)][int(self.above_tile_left.y)] != 0 and self.velocity.y <= 0:
                        self.y = (self.above_tile_left.y + 1) * TILE_SIZE
                        self.velocity.y = 0
                    elif self.tilemap.grid[int(self.above_tile_right.x)][int(self.above_tile_right.y)] != 0 and self.velocity.y <= 0:
                        self.y = (self.above_tile_right.y + 1) * TILE_SIZE
                        self.velocity.y = 0

                    self.right_tile_top = self.tilemap.world_to_tile(self.dx, (self.y + self.height * 0.5) - 1)
                    self.right_tile_bottom = self.tilemap.world_to_tile(self.dx, (self.y + self.height * 0.5) + 1)
                    if self.tilemap.grid[int(self.right_tile_top.x)][int(self.right_tile_top.y)] != 0 and self.velocity.x >= 0:
                        self.x = self.right_tile_top.x * TILE_SIZE - self.width
                        self.velocity.x = 0
                        self.is_on_wall = True
                    elif self.tilemap.grid[int(self.right_tile_bottom.x)][int(self.right_tile_bottom.y)] != 0 and self.velocity.x >= 0:
                        self.x = self.right_tile_bottom.x * TILE_SIZE - self.width
                        self.velocity.x = 0
                        self.is_on_wall = True

                    self.left_tile_top = self.tilemap.world_to_tile(self.x, (self.y + self.height * 0.5) - 1)
                    self.left_tile_bottom = self.tilemap.world_to_tile(self.x, (self.y + self.height * 0.5) + 1)
                    if self.tilemap.grid[int(self.left_tile_top.x)][int(self.left_tile_top.y)] != 0 and self.velocity.x <= 0: 
                        self.x = (self.left_tile_top.x + 1) * TILE_SIZE
                        self.velocity.x = 0
                        self.is_on_wall = True
                    elif self.tilemap.grid[int(self.left_tile_bottom.x)][int(self.left_tile_bottom.y)] != 0 and self.velocity.x <= 0: 
                        self.x = (self.left_tile_bottom.x + 1) * TILE_SIZE
                        self.velocity.x = 0
                        self.is_on_wall = True

                    # Collision with world borders
                    if self.x < 0:
                        self.x = 0
                        self.velocity.x = 0
                    elif self.dx > self.limit_right and self.can_collide_end:
                        self.x = self.limit_right - self.width
                        self.velocity.x = 0
                    if self.y < 0:
                        self.y = 0
                        self.velocity.y = 0

                if self.y > self.limit_bottom:
                    self.kill()
                
                if self.is_on_ground: self.jumping = False

                if self.is_on_wall and self.direction != 0 and self.velocity.y > 0 and self.can_wall_jump:
                    self.velocity.y = 0.4
                    self.wall_jumping = True
                    self.jumping = False
                elif not self.is_on_ground:
                    self.can_jump = False

                if self.want_to_jump and self.can_jump:
                    self.can_jump = False
                    self.want_to_jump = False
                    if self.wall_jumping and self.can_wall_jump: self.velocity.y = self.jump_force * 0.5
                    else: self.velocity.y = self.jump_force
                    if self.wall_jumping and self.can_wall_jump:
                        self.velocity.x = 3.5 * (self.direction / -1)
                    self.jumping = True
                elif self.want_to_jump == False and self.velocity.y < 0 and self.jumping:
                    self.velocity.y *= self.jump_cancel_factor

            else:
                pass

            self.rect.x = self.x - camera.x
            self.rect.y = self.y - camera.y

            self.draw_pos = (self.rect.x, self.rect.y)

    def draw(self, viewport):
        pygame.draw.rect(viewport, (255,0,0), self.rect)