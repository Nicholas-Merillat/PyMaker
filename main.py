from settings import *

from game_state import GameState
from editor import Editor
from level import Level
from main_menu import MainMenu
from settings_menu import SettingsMenu

# Have to call this or else fetching monitor resolution doesn't work on some displays (eg my monitor at home bruh)
if os.name == 'nt':
    ctypes.windll.user32.SetProcessDPIAware()

class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('PyMaker')
        pygame.display.set_icon(pygame.image.load('content/images/icon.png'))
        self.display_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        self.viewport = pygame.Surface(VIEWPORT_RESOLUTION)
        self.canvas = pygame.Surface(WINDOW_RESOLUTION, pygame.SRCALPHA)

        self.fullscreen = False
        self.vsync = VSYNC
        self.screen = pygame.display.set_mode(WINDOW_RESOLUTION, pygame.SCALED, vsync=int(self.vsync))

        self.clock = pygame.time.Clock()

        self.debug_text_color = (255,255,255)
        self.gui_manager = pygame_gui.UIManager(WINDOW_RESOLUTION, theme_path='content/theme.json', enable_live_theme_updates=True)
        self.screen_scale_factor = pygame.math.Vector2(self.screen.size[0] / VIEWPORT_RESOLUTION[0], self.screen.size[1] / VIEWPORT_RESOLUTION[1])

        self.global_level_name = 'Level Name'

        self.states = {'main_menu': MainMenu('main_menu', self), 'settings_menu': SettingsMenu('settings_menu', self), 'level': Level('level', self), 'editor': Editor('editor', self)}
        self.game_state_manager = GameStateManager('main_menu', self)

        # Initialize text and screen scale factor
        self.refresh_screen()

    def draw(self):
        # Draw any pixel art on viewport to keep pixels
        self.viewport.fill('black')
        self.canvas.fill((255,255,255,0))

        # Draw current game state
        self.states[self.game_state_manager.get_state()].draw()

        # Scale viewport up and blit onto screen for pixel art effect + good performance
        pygame.transform.scale(self.viewport, self.screen.get_size(), self.screen)

        self.gui_manager.draw_ui(self.canvas)

        fps_text = self.font_big.render(f'{int(self.clock.get_fps())}', False, self.debug_text_color)
        self.canvas.blit(fps_text, fps_text.get_rect(topright=(self.canvas.width - 5, 0 * self.screen_scale_factor.y)))

        self.screen.blit(self.canvas, (0,0))

    def refresh_screen(self):
        self.canvas = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.gui_manager.set_window_resolution(self.screen.get_size())
        self.screen_scale_factor = pygame.math.Vector2(self.screen.size[0] / VIEWPORT_RESOLUTION[0], self.screen.size[1] / VIEWPORT_RESOLUTION[1])
        self.font_big = pygame.Font('content/bolds-pixels.ttf', int(24 * self.screen_scale_factor.x))
        self.font_medium = pygame.Font('content/bolds-pixels.ttf', int(16 * self.screen_scale_factor.x))
        self.font_small = pygame.Font('content/bolds-pixels.ttf', int(12 * self.screen_scale_factor.x))
        self.states[self.game_state_manager.get_state()].refresh()


    def toggle_fullscreen(self):
        if main.fullscreen:
            main.fullscreen = False
            main.screen = pygame.display.set_mode(WINDOW_RESOLUTION)
        else:
            main.fullscreen = True
            main.screen = pygame.display.set_mode(self.display_resolution, pygame.FULLSCREEN)
        main.refresh_screen()

    def run(self):
        while True:
            self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS

            for event in pygame.event.get():
                self.gui_manager.process_events(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.game_state_manager.get_state() == 'main_menu':
                        pygame.quit()
                        sys.exit()

                self.states[self.game_state_manager.get_state()].input(event)

            self.mouse_position = pygame.math.Vector2(pygame.mouse.get_pos())
            self.mouse_pressed = pygame.mouse.get_pressed()
            self.keys = pygame.key.get_pressed()

            self.gui_manager.update(self.delta)

            # Run the current game state
            self.states[self.game_state_manager.get_state()].run()
            
            self.draw()
            pygame.display.flip()

class GameStateManager():
    def __init__(self, current_state, main: Main):
        self.main = main

        # Get subclasses from object
        if GameState not in type(self.main.states[current_state]).mro():
            raise TypeError('provided state is not a valid GameState')

        self.main.states[current_state].load()
        self.current_state = current_state

    def get_state(self):
        return self.current_state
    
    def set_state(self, new_state):
        self.main.states[self.current_state].exit()

        if new_state == 'editor':
            self.main.states[new_state].level = Level('level', self.main)
        elif new_state == 'level':
            self.main.states[new_state] = Level('level', self.main)

        self.main.states[new_state].load()
        self.current_state = new_state

if __name__ == '__main__':
    main = Main()
    main.run()