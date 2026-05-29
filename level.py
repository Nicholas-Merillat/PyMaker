from settings import *

from game_state import GameState
from background import Background
from tilemap import TileMap
from player import Player
from camera import Camera
from enemy import Enemy

class Level(GameState):
    def __init__(self, name, main):
        super().__init__(name, main)

        self.debug_view = False
        self.debug_key_pressed = False

        self.guis = []

        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((900, 125), (100, 50)),
                                                    text='Exit',
                                                    manager=self.main.gui_manager)

        self.heart_icon = pygame.transform.scale(pygame.image.load('content/images/heart.png').convert_alpha(), (16 * self.main.screen_scale_factor.x, 16 * self.main.screen_scale_factor.y))

        self.paused = False
        self.pause_key_pressed = False
        self.pause_rect = pygame.transform.scale(pygame.image.load('content/images/black.png').convert_alpha(), self.main.screen.get_size())
        self.pause_rect.set_alpha(150)

        self.camera = Camera(16, 920, self)

        self.background = Background()

        self.tilemap = TileMap(self.camera, self)
        self.tilemap.generate_world()

        self.player = Player(16, 1100, 12, 14, self.tilemap, self)

        self.entities = []

        self.guis.append(self.exit_button)
        for gui in self.guis:
            gui.hide()
            gui.disable()

    def load(self):
        super().load()
        self.tilemap.load_level(self.main.global_level_name)

    def input(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_button:
                self.main.game_state_manager.set_state('main_menu')

        if self.main.keys[pygame.K_ESCAPE]:
            if not self.pause_key_pressed:
                self.pause_key_pressed = True
                self.paused = not self.paused
        else:
            self.pause_key_pressed = False
        
        if self.main.keys[pygame.K_SPACE]:
            if not self.debug_key_pressed:
                self.debug_key_pressed = True
                self.debug_view = not self.debug_view
        else:
            self.debug_key_pressed = False

    def run(self):
        for gui in self.guis:
            if self.main.game_state_manager.get_state() == self.name:
                if gui is self.exit_button and self.paused:
                    gui.show()
                    gui.enable()
                else:
                    gui.hide()
                    gui.disable()
            else:
                gui.hide()
                gui.disable()

        self.exit_button.set_position(((self.main.screen.size[0] * 0.5 - (50 * self.main.screen_scale_factor.x) * 0.5), 265 * self.main.screen_scale_factor.y))
        self.exit_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.entities = self.tilemap.enemies + self.tilemap.items

        self.mouse_position_tile = self.tilemap.screen_to_tile((self.main.mouse_position.x / self.main.screen_scale_factor.x), (self.main.mouse_position.y / self.main.screen_scale_factor.y))

        self.tilemap.update(self.mouse_position_tile, self.main.mouse_pressed, self.main.keys)
        
        self.entities = [entity for entity in self.entities if entity.alive]
        for entity in self.entities:
            if type(entity) is Enemy:
                entity.update(self.main.delta, self.camera, pygame.Vector2(self.player.x, self.player.y))
            else:
                entity.update(self.main.delta, self.camera)

        self.camera.update(self.main.delta, self.player)
        self.player.update(self.main.delta, self.camera, self.main.keys)
        self.background.update(self.camera)

    def draw(self):
        self.main.viewport.blit(self.background.surface, pygame.Vector2(0,0))

        self.tilemap.draw(self.main.viewport, self.camera)

        cherry_text = self.main.font_medium.render(f'Cherries: {self.player.cherries}', False, (255,255,255))
        lives_text = self.main.font_medium.render(f'Lives: {self.player.lives}', False, (255,255,255))
        self.main.canvas.blit(cherry_text, cherry_text.get_rect(bottomleft=(5 * self.main.screen_scale_factor.x, self.main.screen.size[1])))
        self.main.canvas.blit(lives_text, lives_text.get_rect(bottomleft=(5 * self.main.screen_scale_factor.x, self.main.screen.size[1] - 16 * self.main.screen_scale_factor.y)))
        if self.player.health > 0: self.main.canvas.blit(self.heart_icon, (3 * self.main.screen_scale_factor.x, self.main.screen.size[1] - 50 * self.main.screen_scale_factor.y))
        if self.player.health > 1: self.main.canvas.blit(self.heart_icon, (24 * self.main.screen_scale_factor.x, self.main.screen.size[1] - 50 * self.main.screen_scale_factor.y))
        if self.player.health > 2: self.main.canvas.blit(self.heart_icon, (45 * self.main.screen_scale_factor.x, self.main.screen.size[1] - 50 * self.main.screen_scale_factor.y))

        for entity in self.entities:
            entity.draw(self.main.viewport)
            if self.debug_view: pygame.draw.rect(self.main.viewport, (255,0,0), entity.rect)

        self.player.draw(self.main.viewport)
        if self.debug_view: 
            pygame.draw.rect(self.main.viewport, (0,0,255), self.player.bounding_rect)
            pygame.draw.rect(self.main.viewport, (255,0,0), self.player.rect)

        if self.paused:
            self.main.canvas.blit(self.pause_rect, (0,0))
            pause_text = self.main.font_big.render('Paused', False, (255,255,255))
            self.main.canvas.blit(pause_text, pause_text.get_rect(center=(self.main.screen.size[0] * 0.5, self.main.screen.size[1] * 0.5 - 50 * self.main.screen_scale_factor.x)))

    def refresh(self):
        self.heart_icon = pygame.transform.scale(self.heart_icon, (16 * self.main.screen_scale_factor.x, 16 * self.main.screen_scale_factor.y))

    def exit(self):
        for gui in self.guis:
            gui.hide()
            gui.disable()