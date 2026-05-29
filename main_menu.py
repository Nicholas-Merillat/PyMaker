from settings import *

from game_state import GameState

class MainMenu(GameState):
    def __init__(self, name, main):
        super().__init__(name, main)

        self.level_text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.main.screen.size[0] * 0.5 - 100, 320), (200, 50)),
                                                    initial_text=f'{self.main.global_level_name}',
                                                    manager=self.main.gui_manager)
        
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((900, 100), (100, 50)),
                                                    text='Play',
                                                    manager=self.main.gui_manager)
        self.edit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((900, 125), (100, 50)),
                                                    text='Edit',
                                                    manager=self.main.gui_manager)
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((900, 125), (100, 50)),
                                                    text='Settings',
                                                    manager=self.main.gui_manager)
        
        self.guis = []
        self.guis.append(self.level_text_box)
        self.guis.append(self.play_button)
        self.guis.append(self.edit_button)
        self.guis.append(self.settings_button)
        for gui in self.guis:
            gui.hide()
            gui.disable()

    def load(self):
        super().load()

    def input(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.main.game_state_manager.set_state('level')
            elif event.ui_element == self.edit_button:
                self.main.game_state_manager.set_state('editor')
            elif event.ui_element == self.settings_button:
                self.main.game_state_manager.set_state('settings_menu')

    def run(self):
        for gui in self.guis:
            if self.main.game_state_manager.get_state() == self.name:
                gui.show()
                gui.enable()
            else:
                gui.hide()
                gui.disable()

        self.main.global_level_name = self.level_text_box.text

        self.level_text_box.set_position(((self.main.screen.size[0] * 0.5 - (100 * self.main.screen_scale_factor.x) * 0.5), 160 * self.main.screen_scale_factor.y))
        self.level_text_box.set_dimensions((100 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.play_button.set_position(((self.main.screen.size[0] * 0.5 - (50 * self.main.screen_scale_factor.x) * 0.5), 200 * self.main.screen_scale_factor.y))
        self.play_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.edit_button.set_position(((self.main.screen.size[0] * 0.5 - (50 * self.main.screen_scale_factor.x) * 0.5), 230 * self.main.screen_scale_factor.y))
        self.edit_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.settings_button.set_position(((self.main.screen.size[0] * 0.5 - (55 * self.main.screen_scale_factor.x) * 0.5), 260 * self.main.screen_scale_factor.y))
        self.settings_button.set_dimensions((55 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))
    
    def draw(self):
        title_text = self.main.font_big.render('PyMaker', False, (255,255,255))
        self.main.canvas.blit(title_text, title_text.get_rect(center=(self.main.screen.size[0] * 0.5, self.main.screen.size[1] * 0.5 - 50 * self.main.screen_scale_factor.x)))

    def refresh(self):
        pass

    def exit(self):
        for gui in self.guis:
            gui.hide()
            gui.disable()