import rocket
import bullet
import pygame
import asteroid
import random


class GameObjectsLogic:
    def __init__(self, screen):
        self._screen = screen
        self.rocket = rocket.Rocket(400, 300, screen)
        self.active_bullets = []
        self.active_asteroids = [asteroid.Asteroid(self._screen, 0, random.randint(0, screen.get_rect().width),
                                                   random.randint(0, screen.get_rect().height)),
                                 asteroid.Asteroid(self._screen, 1, random.randint(0, screen.get_rect().width),
                                                   random.randint(0, screen.get_rect().height)),
                                 asteroid.Asteroid(self._screen, 2, random.randint(0, screen.get_rect().width),
                                                   random.randint(0, screen.get_rect().height))]
        self._last_time_fired = 0

    def fire(self):
        if pygame.time.get_ticks() - self._last_time_fired >= 300:
            self.active_bullets.append(bullet.Bullet(self.rocket.rotated_rect.centerx,
                                                     self.rocket.rotated_rect.centery,
                                                     self.rocket.rotation_angle,
                                                     self._screen.get_rect().size))
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

    def bullet_hit_asteroid(self):
        bul_to_destroy = []
        astr_to_destroy = []
        for i in range(len(self.active_bullets)):
            for j in range(len(self.active_asteroids)):
                if self.active_asteroids[j].image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                                    self.active_bullets[i].cur_y):
                    self.rocket.score += 10
                    bul_to_destroy.append(i)
                    astr_to_destroy.append(j)
        for i in bul_to_destroy:
            del self.active_bullets[i]
        for i in astr_to_destroy:
            astr = self.active_asteroids[i]
            if astr.size > 0:
                self.active_asteroids.append(asteroid.Asteroid(self._screen, astr.size - 1,
                                                               astr.image_rect.x, astr.image_rect.y))
                self.active_asteroids.append(asteroid.Asteroid(self._screen, astr.size - 1,
                                                               astr.image_rect.x, astr.image_rect.y))
            del self.active_asteroids[i]

    def rocket_hit_asteroid(self):
        for aster in self.active_asteroids:
            if self.rocket.image_rect.colliderect(aster.image_rect):
                return True
        return False
