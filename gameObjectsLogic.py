import rocket
import bullet
import pygame
import asteroid
import random
import ufo


class GameObjectsLogic:
    def __init__(self, screen):
        self._screen = screen
        self.rocket = rocket.Rocket(400, 300, screen)
        self.active_bullets = []
        self.active_asteroids = [asteroid.Asteroid(self._screen, 2,
                                                   random.randint(0, screen.get_rect().width),
                                                   random.randint(0, screen.get_rect().height)),
                                 asteroid.Asteroid(self._screen, 2,
                                                   random.randint(0, screen.get_rect().width),
                                                   random.randint(0, screen.get_rect().height)),
                                 asteroid.Asteroid(self._screen, 2,
                                                   random.randint(0, screen.get_rect().width),
                                                   random.randint(0, screen.get_rect().height))]
        self._last_time_rocket_fired = 0
        self._time_ufo_was_destroyed = 0
        self._last_time_ufo_fired = 0
        self._amount_asteroids = len(self.active_asteroids)
        self.ufo = None
        self.rocket_destroyed = False
        self.lives = 3

    def update(self):
        self._spawn_ufo()
        self._update_rocket()
        self._update_ufo()
        self._update_bullets()
        self._update_asteroids()
        self._ufo_fire()
        self._bullet_hit_smth()
        self._bullet_hit_ufo()
        self._ufo_hit_asteroid()
        self._rocket_hit_other_obj()
        print(len(self.active_asteroids))
        if not len(self.active_asteroids):
            self._level_restart()

    def _level_restart(self):
        self._amount_asteroids = min(self._amount_asteroids + 2, 7)
        self.rocket.make_invincible()
        for _ in range(self._amount_asteroids):
            self.active_asteroids.append(asteroid.Asteroid(self._screen, 2,
                                                           random.randint(0, self._screen.get_rect().width),
                                                           random.randint(0, self._screen.get_rect().height)))

    def fire(self):
        if pygame.time.get_ticks() - self._last_time_rocket_fired >= 300:
            self.active_bullets.append(bullet.Bullet(self.rocket.rotated_rect.centerx,
                                                     self.rocket.rotated_rect.centery,
                                                     self.rocket.rotation_angle,
                                                     self._screen.get_rect().size,
                                                     True))
            self._last_time_rocket_fired = pygame.time.get_ticks()

    def _ufo_fire(self):
        if self.ufo is not None:
            if pygame.time.get_ticks() - self._last_time_ufo_fired >= 1000:
                self.active_bullets.append(bullet.Bullet(self.ufo.image_rect.centerx,
                                                         self.ufo.image_rect.centery,
                                                         random.randint(0, 360),
                                                         self._screen.get_rect().size,
                                                         False))
                self._last_time_ufo_fired = pygame.time.get_ticks()

    def _spawn_ufo(self):
        if self.ufo is None and pygame.time.get_ticks() - self._time_ufo_was_destroyed >= 15000:
            self.ufo = ufo.UFO(screen=self._screen)
            self._last_time_ufo_fired = pygame.time.get_ticks()

    def _update_rocket(self):
        if self.lives >= 1 and self.rocket_destroyed:
            self.rocket.respawn()
            self.lives -= 1
            self.rocket_destroyed = False
        else:
            self.rocket.get_next_frame_coordinates()
            if self.rocket.is_invincible():
                if pygame.time.get_ticks() % 4:
                    self._screen.blit(self.rocket.rotated_image, self.rocket.rotated_rect)
            else:
                self._screen.blit(self.rocket.rotated_image, self.rocket.rotated_rect)

    def _update_bullets(self):
        far_bullets = []
        for i in range(len(self.active_bullets)):
            if self.active_bullets[i].is_far_enough():
                far_bullets.append(i)
            else:
                self.active_bullets[i].update(self._screen)
        for i in far_bullets:
            del self.active_bullets[i]

    def _update_asteroids(self):
        for aster in self.active_asteroids:
            aster.update()

    def _update_ufo(self):
        if self.ufo:
            self.ufo.update()

    def _bullet_hit_smth(self):
        bul_to_destroy = set()
        aster_to_destroy = set()
        for i in range(len(self.active_bullets)):
            for j in range(len(self.active_asteroids)):
                if j in aster_to_destroy:
                    continue
                if self.active_asteroids[j].image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                                    self.active_bullets[i].cur_y):
                    if self.active_bullets[i].rocket_fired:
                        self.rocket.score += 10
                    bul_to_destroy.add(i)
                    aster_to_destroy.add(j)
            if i not in bul_to_destroy:
                if self.ufo is not None and \
                        self.active_bullets[i].rocket_fired and \
                        self.ufo.image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                         self.active_bullets[i].cur_y):
                    self._time_ufo_was_destroyed = pygame.time.get_ticks()
                    self.ufo = None
                    self.rocket.score += 20
                elif not (self.rocket.is_invincible() or self.rocket_destroyed) and \
                        not self.active_bullets[i].rocket_fired and \
                        self.rocket.image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                            self.active_bullets[i].cur_y):
                    self.rocket_destroyed = True

        self._clear_bullets(bul_to_destroy)
        self._clear_aster(aster_to_destroy)

    def _clear_bullets(self, bul_indexes):
        bi = list(bul_indexes)
        bi.sort(reverse=True)
        for i in bi:
            self.active_bullets.pop(i)

    def _clear_aster(self, aster_indexes):
        ai = list(aster_indexes)
        ai.sort(reverse=True)
        for i in ai:
            aster = self.active_asteroids.pop(i)
            if aster.size > 0:
                self.active_asteroids.append(asteroid.Asteroid(self._screen, aster.size - 1,
                                                               aster.image_rect.x, aster.image_rect.y))
                self.active_asteroids.append(asteroid.Asteroid(self._screen, aster.size - 1,
                                                               aster.image_rect.x, aster.image_rect.y))

    def _rocket_hit_other_obj(self):
        if self.rocket.is_invincible() or self.rocket_destroyed:
            pass
        elif self.ufo is not None and self.rocket.image_rect.colliderect(self.ufo.image_rect):
            self.rocket_destroyed = True
            pass
        else:
            for aster in self.active_asteroids:
                if self.rocket.image_rect.colliderect(aster.image_rect):
                    self.rocket_destroyed = True

    def _bullet_hit_ufo(self):
        if self.ufo is not None:
            bul_to_destroy = -1
            for i in range(len(self.active_bullets)):
                if self.active_bullets[i].rocket_fired and \
                        self.ufo.image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                         self.active_bullets[i].cur_y):
                    self._time_ufo_was_destroyed = pygame.time.get_ticks()
                    bul_to_destroy = i
                    self.ufo = None
                    self.rocket.score += 20
                    break
            if bul_to_destroy != -1:
                self.active_bullets.pop(bul_to_destroy)

    def _ufo_hit_asteroid(self):
        if self.ufo is not None:
            aster_to_destroy = -1
            for i in range(len(self.active_asteroids)):
                if self.ufo.image_rect.colliderect(self.active_asteroids[i].image_rect):
                    self._time_ufo_was_destroyed = pygame.time.get_ticks()
                    self.ufo = None
                    aster_to_destroy = i
                    break
            if aster_to_destroy != -1:
                self.active_asteroids.pop(aster_to_destroy)
