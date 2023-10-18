import rocket
import bullet
import pygame
import asteroid


class GameObjectsLogic:
    def __init__(self, screen):
        self._screen = screen
        self.rocket = rocket.Rocket(400, 300)
        self.active_bullets = []
        self.active_asteroids = [asteroid.Asteroid(self._screen),
                                 asteroid.Asteroid(self._screen),
                                 asteroid.Asteroid(self._screen)]
        self._last_time_fired = 0

    def fire(self):
        if pygame.time.get_ticks() - self._last_time_fired >= 300:
            self.active_bullets.append(bullet.Bullet(self.rocket.rotated_rect.centerx,
                                                     self.rocket.rotated_rect.centery,
                                                     self.rocket.rotation_angle))
            self._last_time_fired = pygame.time.get_ticks()

    def update_bullets(self):
        far_bullets = []
        for i in range(len(self.active_bullets)):
            if self.active_bullets[i].is_far_enough():
                far_bullets.append(i)
            else:
                self.active_bullets[i].update(self._screen)
        for i in far_bullets:
            del self.active_bullets[i]

    def update_asteroids(self):
        for aster in self.active_asteroids:
            aster.update()
