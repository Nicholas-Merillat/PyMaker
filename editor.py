from settings import *

from game_state import GameState
from level import Level

class Editor(GameState):
    def __init__(self, name, main):
        super().__init__(name, main)

        self.level = Level('level', self.main)

        self.right_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.main.screen.size[0] - 100, -5), (self.main.screen.size[0] + 10, 60)),
            manager=self.main.gui_manager,
            object_id="#right_panel"
        )
        self.top_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((-5, -5), (self.main.screen.size[0] + 10, 60)),
            manager=self.main.gui_manager,
            object_id="#top_panel"
        )

        self.edit_toggle_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((900, 100), (100, 50)),
            text='Edit',
            manager=self.main.gui_manager
            )
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((900, 125), (100, 50)),
            text='Save',
            manager=self.main.gui_manager
            )
        
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((900, 125), (100, 50)),
            text='Exit',
            manager=self.main.gui_manager
            )
        
        # TODO somehow make this automated (maybe with a list of placeable tiles and objects)
        
        self.tile_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 125), (100, 50)),
            text='Ground',
            manager=self.main.gui_manager)
        self.enemy_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 200), (100, 50)),
            text='Opossum',
            manager=self.main.gui_manager)
        self.cherry_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 200), (100, 50)),
            text='Cherry',
            manager=self.main.gui_manager)
        self.block_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 125), (100, 50)),
            text='Block',
            manager=self.main.gui_manager)
        
        self.guis = []
        self.guis.append(self.top_panel)
        self.guis.append(self.right_panel)
        self.guis.append(self.edit_toggle_button)
        self.guis.append(self.save_button)
        self.guis.append(self.exit_button)
        self.guis.append(self.tile_button)
        self.guis.append(self.enemy_button)
        self.guis.append(self.cherry_button)
        self.guis.append(self.block_button)
        for gui in self.guis:
            gui.hide()
            gui.disable()

    def load(self):
        super().load()
        self.level.load()
        self.editing = True

    def input(self, event):
        self.level.input(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.edit_toggle_button:
                self.editing = not self.editing
                if self.editing:
                    self.level.tilemap.enemies.clear()
                    self.level.tilemap.items.clear()
                    self.level.tilemap.load_enemies(self.main.global_level_name)
                    self.level.tilemap.load_items(self.main.global_level_name)
            elif event.ui_element == self.save_button:
                self.level.tilemap.save_level(self.main.global_level_name)
            elif event.ui_element == self.exit_button:
                self.main.game_state_manager.set_state('main_menu')
            elif event.ui_element == self.tile_button:
                self.level.tilemap.is_placing = 'tile'
                self.level.tilemap.current_tile = 1
            elif event.ui_element == self.block_button:
                self.level.tilemap.is_placing = 'tile'
                self.level.tilemap.current_tile = 2
            elif event.ui_element == self.enemy_button:
                self.level.tilemap.is_placing = 'opossum'
            elif event.ui_element == self.cherry_button:
                self.level.tilemap.is_placing = 'cherry'

    def run(self):
        self.level.tilemap.editing = self.editing
        if self.editing: self.level.paused = False

        for gui in self.guis:
            if self.main.game_state_manager.get_state() == self.name:
                gui.show()
                gui.enable()
                if self.level.player.rect.x > 545 and gui is self.right_panel:
                    gui.hide()
                    gui.disable()
                if self.level.player.rect.y < 55 and gui is self.top_panel:
                    gui.hide()
                    gui.disable()
            else:
                gui.hide()
                gui.disable()

        self.edit_toggle_button.set_position((578 * self.main.screen_scale_factor.x, 85 * self.main.screen_scale_factor.y))
        self.edit_toggle_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))
        if self.editing: self.edit_toggle_button.set_text('Play')
        else: self.edit_toggle_button.set_text('Edit')

        self.save_button.set_position((578 * self.main.screen_scale_factor.x, 55 * self.main.screen_scale_factor.y))
        self.save_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.exit_button.set_position((578 * self.main.screen_scale_factor.x, self.main.screen.size[1] - 30 * self.main.screen_scale_factor.y))
        self.exit_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.tile_button.set_position((20 * self.main.screen_scale_factor.x, 10 * self.main.screen_scale_factor.y))
        self.tile_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.block_button.set_position((185 * self.main.screen_scale_factor.x, 10 * self.main.screen_scale_factor.y))
        self.block_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.enemy_button.set_position((75 * self.main.screen_scale_factor.x, 10 * self.main.screen_scale_factor.y))
        self.enemy_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.cherry_button.set_position((130 * self.main.screen_scale_factor.x, 10 * self.main.screen_scale_factor.y))
        self.cherry_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.top_panel.set_position((-10 * self.main.screen_scale_factor.x, -10 * self.main.screen_scale_factor.y))
        self.top_panel.set_dimensions(((self.main.screen.size[0] + 10) * self.main.screen_scale_factor.x, 60 * self.main.screen_scale_factor.y))

        self.right_panel.set_position((self.main.screen.size[0] - 80 * self.main.screen_scale_factor.x, -10 * self.main.screen_scale_factor.y))
        self.right_panel.set_dimensions((150 * self.main.screen_scale_factor.x, self.main.screen.size[1] + 20 * self.main.screen_scale_factor.y))
        self.right_panel.background_colour = pygame.Color(255,255,255)

        self.level.run()

    def draw(self):
        self.level.draw()

    def refresh(self):
        self.level.refresh()

    def exit(self):
        self.level.exit()
        for gui in self.guis:
            gui.hide()
            gui.disable()