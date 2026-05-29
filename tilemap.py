from settings import *

from tileset import TileSet
from enemy import Enemy
from item import Item

class TileMap():
    # I did have ChatGPT convert these Consts and the Dictionary from my C# Tile Project into Python
    # It makes my life a lot easier :)
    NW = 1
    NORTH  = 2
    NE = 4
    WEST  = 8
    EAST  = 16
    SW = 32
    SOUTH  = 64
    SE = 128

    mask_to_tile_dict = {
        2: 1, 8: 2, 10: 3, 11: 4,
        16: 5, 18: 6, 22: 7, 24: 8,
        26: 9, 27: 10, 30: 11, 31: 12,
        64: 13, 66: 14, 72: 15, 74: 16,
        75: 17, 80: 18, 82: 19, 86: 20,
        88: 21, 90: 22, 91: 23, 94: 24,
        95: 25, 104: 26, 106: 27, 107: 28,
        120: 29, 122: 30, 123: 31, 126: 32,
        127: 33, 208: 34, 210: 35, 214: 36,
        216: 37, 218: 38, 219: 39, 222: 40,
        223: 41, 248: 42, 250: 43, 251: 44,
        254: 45, 255: 46, 0: 47
    }
    
    def __init__(self, camera, level):
        self.editing = False
        self.current_tile = 1

        self.cursor = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.cursor.fill((75,75,75))
        self.camera = camera
        self.level = level

        self.grid = numpy.full(TILEMAP_SIZE, 0)

        self.surface = pygame.surface.Surface(VIEWPORT_RESOLUTION, pygame.SRCALPHA)

        self.place_mode = 'tile'
        self.is_placing = 'tile'

        self.object_positions = []
        self.enemies = []
        self.items = []
        self.enemy_count = 0
        self.item_count = 0

        # Load tilesets
        self.tilesets = []
        self.tile_data = []
        with open('content/tiles.txt', 'r') as file:
            file_content = file.read()
            tiles = file_content.splitlines()
            bitmap_index = 0
            
            for tile in tiles:
                bitmap_index = tile.find(':')
                tile_str = tile[0 : bitmap_index]
                tile_can_bitmask = self.str_to_bool(tile[bitmap_index+1: len(tile)])
                if 'air' not in tile_str:
                    image_path = f'content/images/{tile_str}.png'
                    try:
                        surface = pygame.image.load(image_path)
                        surface = surface.convert_alpha()
                        self.tilesets.append(TileSet(tile_str, surface))
                        self.tile_data.append(tile_can_bitmask)
                        print(f'{tile_str}, bitmask {tile_can_bitmask}')
                    except pygame.error as e:
                        print(f'Error loading tileset {tile_str}: {e}')

    def str_to_bool(self, string):
        return string.lower() == 'true'

    # Set tile ID at tile position
    def set_tile(self, tile_x, tile_y, tile_id):
        if tile_x >= TILEMAP_SIZE[0] - 5 and (tile_y <= TILEMAP_SIZE[1] - 6 or tile_y >= TILEMAP_SIZE[1] - 2):
            self.grid[tile_x][tile_y] = 1
        else:
            tile_x = max(0, min(tile_x, TILEMAP_SIZE[0] - 1))
            tile_y = max(0, min(tile_y, TILEMAP_SIZE[1] - 1))
            self.grid[tile_x][tile_y] = tile_id

    # Get tile ID at tile position
    def get_tile(self, tile_x, tile_y):
        return self.grid[tile_x][tile_y]

    # Get world coordinates of a tile with tile position
    def tile_to_world(self, tile_x, tile_y):
        return pygame.math.Vector2(tile_x * TILE_SIZE + self.camera.x, tile_y * TILE_SIZE + self.camera.y)
    
    # Convert screen coordinates to corresponding tile
    def screen_to_tile(self, x, y):
        tile_x = int(math.floor((x + self.camera.x) / TILE_SIZE))
        tile_y = int(math.floor((y + self.camera.y) / TILE_SIZE))
        return pygame.math.Vector2(tile_x, tile_y)
    
    # Convert world coordinates to corresponding tile
    def world_to_tile(self, x, y):
        tile_x = int(math.floor(x / TILE_SIZE))
        tile_y = int(math.floor(y / TILE_SIZE))
        tile_x = max(0, min(tile_x, TILEMAP_SIZE[0] - 1))
        tile_y = max(0, min(tile_y, TILEMAP_SIZE[1] - 1))
        return pygame.math.Vector2(tile_x, tile_y)
    
    def generate_world(self):
        for y in range(TILEMAP_SIZE[1]):
            for x in range(TILEMAP_SIZE[0]):
                if y >= TILEMAP_SIZE[1] - 2:
                    self.set_tile(x, y, 1)

                if x >= TILEMAP_SIZE[0] - 5 and (y <= TILEMAP_SIZE[1] - 6 or y >= TILEMAP_SIZE[1] - 2):
                    self.set_tile(x, y, 1)

    def save_level(self, name):
        if not os.path.isdir('saves'):
            os.makedirs('saves', exist_ok=True)

        try:
            os.makedirs(f'saves/{name}', exist_ok=True)
            numpy.savetxt(f'saves/{name}/grid.txt', self.grid, delimiter=',', fmt='%d')
            with open(f'saves/{name}/enemies.txt', 'w') as file:
                for enemy in self.enemies:
                    file.write(f'{int(enemy.spawn_x),int(enemy.spawn_y)}\n')
            with open(f'saves/{name}/items.txt', 'w') as file:
                for item in self.items:
                    file.write(f'{int(item.spawn_x),int(item.spawn_y)}\n')
        except:
            return False
        return True

    def load_level(self, name):
        if os.path.isdir(f'saves/{name}'):
            self.grid = numpy.loadtxt(f'saves/{name}/grid.txt', delimiter=',', dtype=int)
            self.load_enemies(name)
            self.load_items(name)
            print(f'loaded level "{name}"')
        else:
            print('level does not exist')
            return
        
    def load_enemies(self, name):
        try:
            with open(f'saves/{name}/enemies.txt', 'r') as file:
                file_content = file.read()
                enemy_positions = file_content.splitlines()
                positions = []
                for position in enemy_positions:
                    positions.append(ast.literal_eval(position))
                for enemy in positions:
                    self.spawn_enemy(enemy[0], enemy[1])
        except:
            print('enemies.txt does not exist')

    def load_items(self, name):
        try:
            with open(f'saves/{name}/items.txt', 'r') as file:
                file_content = file.read()
                item_positions = file_content.splitlines()
                positions = []
                for position in item_positions:
                    positions.append(ast.literal_eval(position))
                for item in positions:
                    self.spawn_item(item[0], item[1])
        except:
            print('items.txt does not exist')
        
    def spawn_enemy(self, x, y):
        self.enemies.append(Enemy(x, y, 20, 14, 'opossum', self, self.level))
        self.object_positions.append(pygame.Vector2(x, y))
        self.enemy_count += 1

    def delete_enemy(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                enemy.kill()
                self.enemies.remove(enemy)
                self.object_positions.remove(self.mouse_position_world)
                self.enemy_count -= 1
                break

    def spawn_item(self, x, y):
        self.items.append(Item(x, y, 15, 15, 'cherry', self, self.level))
        self.object_positions.append(pygame.Vector2(x, y))
        self.item_count += 1
    
    def delete_item(self, x, y):
        for item in self.items:
            if item.x == x and item.y == y:
                item.kill()
                self.items.remove(item)
                self.object_positions.remove(self.mouse_position_world)
                self.item_count -= 1
                break

    # Direct backport from my C# Tile Project
    def get_mask(self, x, y, tile_id):
        def check(dx, dy):
            nx = x + dx
            ny = y + dy

            if (nx < 0 or ny < 0 or nx >= TILEMAP_SIZE[0] or ny >= TILEMAP_SIZE[1]):
                return True
            
            return self.get_tile(nx, ny) == tile_id

        mask = 0

        n = check(0, -1)
        e = check(1, 0)
        s = check(0, 1)
        w = check(-1, 0)

        # Cardinals
        if n: mask |= TileMap.NORTH
        if e: mask |= TileMap.EAST
        if s: mask |= TileMap.SOUTH
        if w: mask |= TileMap.WEST

        # Diagonals
        if (n and w and check(-1, -1)): mask |= TileMap.NW
        if (n and e and check(1, -1)): mask |= TileMap.NE
        if (s and w and check(-1, 1)): mask |= TileMap.SW
        if (s and e and check(1, 1)): mask |= TileMap.SE

        return mask
    
    def update(self, mouse_position, mouse_pressed, keys):
        self.mouse_position = mouse_position
        self.mouse_position_world = self.mouse_position * TILE_SIZE

        if self.editing:
            if mouse_pressed[0]:
                if self.mouse_position_world in self.object_positions:
                        self.delete_enemy(self.mouse_position_world.x, self.mouse_position_world.y)
                        self.delete_item(self.mouse_position_world.x, self.mouse_position_world.y)
                self.set_tile(int(self.mouse_position.x), int(self.mouse_position.y), 0)
            elif mouse_pressed[2]:
                if self.is_placing == 'opossum':
                    if self.mouse_position_world not in self.object_positions:
                        self.spawn_enemy(self.mouse_position_world.x, self.mouse_position_world.y)
                elif self.is_placing == 'cherry':
                    if self.mouse_position_world not in self.object_positions:
                        self.spawn_item(self.mouse_position_world.x, self.mouse_position_world.y)
                else:
                    self.set_tile(int(self.mouse_position.x), int(self.mouse_position.y), self.current_tile)

        self.surface = pygame.surface.Surface(VIEWPORT_RESOLUTION, pygame.SRCALPHA)

        # Range used to see which tiles to render on screen based on what the camera can see
        self.camera_to_tile = self.screen_to_tile(self.camera.x % TILE_SIZE, self.camera.y % TILE_SIZE)
        self.screen_tile_count_x = math.ceil((VIEWPORT_RESOLUTION[0]) / TILE_SIZE)
        self.screen_tile_count_y = math.ceil((VIEWPORT_RESOLUTION[1]) / TILE_SIZE)
        self.visible_tiles_x = range(max(0, int(self.camera_to_tile.x) - 1), min(int(self.camera_to_tile.x + self.screen_tile_count_x) + 1, TILEMAP_SIZE[0]))
        self.visible_tiles_y = range(max(0, int(self.camera_to_tile.y) - 1), min(int(self.camera_to_tile.y + self.screen_tile_count_y) + 1, TILEMAP_SIZE[1]))

        #print(self.enemies)

        # Iterating column major is apparently more memory efficient
        for y in self.visible_tiles_y:
            for x in self.visible_tiles_x:
                tile_id = self.grid[x][y]
                if tile_id >= 1:

                    # Bit masking for auto tiling
                    bitmask = 0
                    
                    if self.tile_data[tile_id - 1]:
                        mask = self.get_mask(x, y, tile_id)
                        if self.mask_to_tile_dict.get(mask) is not None:
                            bitmask = self.mask_to_tile_dict.get(mask)
                        else:
                            bitmask = 47
                    
                    tile = (self.tilesets[tile_id - 1].get_tile_surface(bitmask))
                    self.surface.blit(tile, (math.floor((x * TILE_SIZE) - self.camera.x), math.floor((y * TILE_SIZE)  - self.camera.y), TILE_SIZE, TILE_SIZE))

    def draw(self, viewport, camera):
        viewport.blit(self.surface, (0,0))
        if self.editing: viewport.blit(self.cursor, (self.mouse_position.x * TILE_SIZE - camera.x, self.mouse_position.y * TILE_SIZE - camera.y), special_flags=pygame.BLEND_ADD)