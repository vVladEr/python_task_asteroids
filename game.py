import pygame
import pygame_gui
import gameObjectsLogic
import game_records

pygame.init()
pygame.font.init()
SIZE = WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 0)


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(SIZE)
        self._clock = pygame.time.Clock()
        self._final_score = 0
        self._record_table = game_records.GameStatistics("records")

    def _switch_scene(self, scene):
        self._current_scene = scene

    # region GAME_SCENE

    def _draw_rocket(self, rocket):
        if rocket.is_invincible():
            if pygame.time.get_ticks() % 4:
                rocket.draw(self._screen)
        else:
            rocket.draw(self._screen)

    def _game_scene(self):
        self._final_score = 0
        self._screen.fill(BLACK)
        f = pygame.font.SysFont('arial', 48)
        objects = gameObjectsLogic.GameObjectsLogic(self._screen.get_size())
        rocket = objects.rocket
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                rocket.increase_speed()
            if pressed[pygame.K_LEFT]:
                rocket.turn_left()
            if pressed[pygame.K_RIGHT]:
                rocket.turn_right()
            if pressed[pygame.K_SPACE]:
                objects.fire()

            self._screen.fill(BLACK)
            objects.update()
            self._draw_rocket(rocket)
            objs_to_draw = objects.get_all_objects()
            for obj in objs_to_draw:
                obj.draw(self._screen)
            score_text = f.render(f"Score:{rocket.score}", True, WHITE)
            lives_text = f.render(f"Lives:{objects.lives}", True, WHITE)
            self._screen.blit(score_text, (10, 10))
            self._screen.blit(lives_text, (10, 60))

            if objects.lives == 0:
                done = True
                self._final_score = rocket.score
                self._switch_scene(self._end_scene)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
    # endregion

    # region END_SCENE
    def _write_endgame_text(self):
        self._screen.fill(BLACK)
        f = pygame.font.SysFont('arial', 56)
        score_text = f.render(f"Your score is {self._final_score}", True, WHITE)
        game_over_text = f.render("GAME OVER", True, WHITE)
        self._screen.blit(game_over_text, (WIDTH // 2 - 160, 100))
        self._screen.blit(score_text, (WIDTH // 2 - 170, 160))
        pygame.display.flip()

    def _end_scene(self):
        self._write_endgame_text()
        gui_manager = pygame_gui.UIManager(SIZE)
        restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 80), (150, 50)),
            text='Restart',
            manager=gui_manager)
        menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 140), (150, 50)),
            text='Back to menu',
            manager=gui_manager)
        record_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 200), (150, 50)),
            text='Records',
            manager=gui_manager)
        text_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((WIDTH // 2 - 160, HEIGHT // 2), (320, 40)),
            manager=gui_manager,
            placeholder_text="Enter your nickname to save your score"
        )
        text_box.unfocus()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        player_name = text_box.get_text()
                        player_name = player_name.strip().replace("\n", "")
                        if player_name == "":
                            self._record_table.save_record(self._final_score, "Unknown pilot")
                        else:
                            self._record_table.save_record(self._final_score, player_name)
                        if event.ui_element == restart_button:
                            done = True
                            self._switch_scene(self._game_scene)
                        if event.ui_element == menu_button:
                            done = True
                            self._switch_scene(self._start_menu_scene)
                        if event.ui_element == record_button:
                            done = True
                            self._switch_scene(self._record_table_scene)
                gui_manager.process_events(event)
            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))
    # endregion

    # region START_MENU
    def _write_start_menu_text(self):
        self._screen.fill(BLACK)
        f = pygame.font.SysFont('arial', 100)
        game_name_text = f.render(f"ASTEROIDS", True, WHITE)
        self._screen.blit(game_name_text, (400, HEIGHT // 2 - 60))
        pygame.display.flip()

    def _start_menu_scene(self):
        self._write_start_menu_text()
        gui_manager = pygame_gui.UIManager(SIZE)
        start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 80), (300, 50)),
            text='Start',
            manager=gui_manager)
        record_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 140), (300, 50)),
            text='Records',
            manager=gui_manager)
        exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 200), (300, 50)),
            text='Exit',
            manager=gui_manager)
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == start_button:
                            done = True
                            self._switch_scene(self._game_scene)
                        if event.ui_element == exit_button:
                            done = True
                            self._switch_scene(None)
                        if event.ui_element == record_button:
                            done = True
                            self._switch_scene(self._record_table_scene)
                gui_manager.process_events(event)
            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))
    # endregion

    # region RECORD_SCENE
    def _record_table_scene(self):
        self._screen.fill(BLACK)
        f = pygame.font.SysFont('arial', 48)
        header_font = pygame.font.SysFont('arial', 80)
        header = header_font.render("RECORDS", True, WHITE)
        self._screen.blit(header, (WIDTH / 2 - 200, 50))
        records = self._record_table.get_records()
        gui_manager = pygame_gui.UIManager(SIZE)
        for i in range(min(len(records), 15)):
            record = records[i]
            text_line = f"{record[0]}:{(19-len(record[0])) * ' '}{record[1]}"
            text = f.render(text_line, True, WHITE)
            self._screen.blit(text, (WIDTH / 2 - 200, HEIGHT / 4 + i * 56))
        menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT - 50), (150, 50)),
            text='Back to menu',
            manager=gui_manager)
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == menu_button:
                            done = True
                            self._switch_scene(self._start_menu_scene)
                gui_manager.process_events(event)
            gui_manager.draw_ui(self._screen)
            pygame.display.flip()
            gui_manager.update(pygame.time.Clock().tick(60))
    # endregion

    def run(self):
        self._switch_scene(self._start_menu_scene)
        while self._current_scene is not None:
            self._current_scene()
        pygame.quit()


