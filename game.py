import pygame
import gameObjectsLogic

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

    def _switch_scene(self, scene):
        self._current_scene = scene

    # region GAME_SCENE
    def _game_scene(self):
        f = pygame.font.SysFont('arial', 48)
        objects = gameObjectsLogic.GameObjectsLogic(self._screen)
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
            score_text = f.render(f"Score:{rocket.score}", True, WHITE)
            lives_text = f.render(f"Lives:{objects.lives}", True, WHITE)
            self._screen.blit(score_text, (10, 10))
            self._screen.blit(lives_text, (10, 60))

            if objects.lives == 0:
                done = True
                self._final_score = rocket.score
                self._switch_scene(self._end_scene)
            pygame.display.flip()
            self._clock.tick(60)
        # endregion

    # region END_SCENE
    def _write_endgame_text(self):
        self._screen.fill(BLACK)
        f = pygame.font.SysFont('arial', 56)
        score_text = f.render(f"Your score is {self._final_score}", True, WHITE)
        game_over_text = f.render("GAME OVER", True, WHITE)
        self._screen.blit(game_over_text, (WIDTH // 2 - 160, HEIGHT // 2 - 60))
        self._screen.blit(score_text, (WIDTH // 2 - 180, HEIGHT // 2))
        pygame.display.flip()

    def _end_scene(self):
        self._write_endgame_text()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.flip()
    # endregion

    def run(self):
        self._switch_scene(self._game_scene())
        while self._current_scene is not None:
            self._current_scene()
        pygame.quit()


