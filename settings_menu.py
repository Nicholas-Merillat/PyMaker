from settings import *

from game_state import GameState

# VSYNC toggle is turned off because pygame doesn't like switching screen modes with vsync on

class SettingsMenu(GameState):
    def __init__(self, name, main):
        super().__init__(name, main)
        
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((900, 100), (100, 50)),
                                                    text='Back',
                                                    manager=self.main.gui_manager)
        self.vsync_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((900, 125), (100, 50)),
                                                    text='Vsync',
                                                    manager=self.main.gui_manager)
        self.fullscreen_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((900, 125), (100, 50)),
                                                    text='Fullscreen',
                                                    manager=self.main.gui_manager)
        if self.main.fullscreen:
            self.fullscreen_button.set_text('Windowed')
        else:
            self.fullscreen_button.set_text('Fullscreen')
        
        self.guis = []
        self.guis.append(self.back_button)
        self.guis.append(self.vsync_button)
        self.guis.append(self.fullscreen_button)
        for gui in self.guis:
            gui.hide()
            gui.disable()

    def load(self):
        super().load()

    def input(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.main.game_state_manager.set_state('main_menu')
            elif event.ui_element == self.vsync_button:
                self.main.vsync = not self.main.vsync
                self.main.refresh_screen()
            elif event.ui_element == self.fullscreen_button:
                self.main.toggle_fullscreen()
                if self.main.fullscreen:
                    self.fullscreen_button.set_text('Windowed')
                else:
                    self.fullscreen_button.set_text('Fullscreen')

    def run(self):
        for gui in self.guis:
            if self.main.game_state_manager.get_state() == self.name:
                gui.show()
                gui.enable()
                if gui is self.vsync_button:
                    gui.disable()
            else:
                gui.hide()
                gui.disable()

        self.back_button.set_position(((self.main.screen.size[0] * 0.5 - (50 * self.main.screen_scale_factor.x) * 0.5), 260 * self.main.screen_scale_factor.y))
        self.back_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.vsync_button.set_position(((self.main.screen.size[0] * 0.5 - (50 * self.main.screen_scale_factor.x) * 0.5), 230 * self.main.screen_scale_factor.y))
        self.vsync_button.set_dimensions((50 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))

        self.fullscreen_button.set_position(((self.main.screen.size[0] * 0.5 - (65 * self.main.screen_scale_factor.x) * 0.5), 200 * self.main.screen_scale_factor.y))
        self.fullscreen_button.set_dimensions((65 * self.main.screen_scale_factor.x, 25 * self.main.screen_scale_factor.y))
    
    def draw(self):
        settings_text = self.main.font_big.render('Settings', False, (255,255,255))
        self.main.canvas.blit(settings_text, settings_text.get_rect(center=(self.main.screen.size[0] * 0.5, self.main.screen.size[1] * 0.5 - 50 * self.main.screen_scale_factor.x)))

    def refresh(self):
        pass

    def exit(self):
        for gui in self.guis:
            gui.hide()
            gui.disable()