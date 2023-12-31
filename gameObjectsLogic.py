import rocket
import bullet
import pygame
import asteroid
import random
import ufo
import supply_capsule


class GameObjectsLogic:
    def __init__(self, screen_size, hard_mode=False):
        self.size = self.width, self.height = screen_size
        self.rocket = rocket.Rocket(400, 300, hard_mode)
        self.active_bullets = []
        self.active_asteroids = [asteroid.Asteroid(2,
                                                   random.randint(0, self.width),
                                                   random.randint(0, self.height))]
        self.collectible_objects = set()
        self._last_time_rocket_fired = pygame.time.get_ticks()
        self._time_ufo_was_destroyed = pygame.time.get_ticks()
        self._last_time_ufo_fired = pygame.time.get_ticks()
        self._amount_asteroids = len(self.active_asteroids)
        self.ufo = None
        self.rocket_destroyed = False
        self.lives = 3
        self._capsule_timeout = 3000
        self._last_time_capsule_spawned = pygame.time.get_ticks()

    def get_all_objects(self):
        objects = set()
        for aster in self.active_asteroids:
            objects.add(aster)
        for bullet in self.active_bullets:
            objects.add(bullet)
        if self.ufo:
            objects.add(self.ufo)
        for obj in self.collectible_objects:
            objects.add(obj)
        return objects

    def update(self):
        self._update_rocket()
        self._update_ufo()
        self._update_bullets()
        self._update_asteroids()
        if len(self.active_asteroids) == 0:
            self._level_restart()

    def _level_restart(self):
        self._amount_asteroids = min(self._amount_asteroids + 2, 7)
        self.rocket.make_invincible()
        for _ in range(self._amount_asteroids):
            self.active_asteroids.append(asteroid.Asteroid(2,
                                                           random.randint(0, self.width),
                                                           random.randint(0, self.height)))

    def fire(self):
        if pygame.time.get_ticks() - self._last_time_rocket_fired >= 150 and self.rocket.is_enough_ammo():
            self.active_bullets.append(bullet.Bullet(self.rocket.rotated_rect.centerx,
                                                     self.rocket.rotated_rect.centery,
                                                     self.rocket.rotation_angle,
                                                     True))
            self._last_time_rocket_fired = pygame.time.get_ticks()
            self.rocket.fire()

    def _ufo_fire(self):
        if self.ufo is not None:
            if pygame.time.get_ticks() - self._last_time_ufo_fired >= 1000:
                self.active_bullets.append(bullet.Bullet(self.ufo.image_rect.centerx,
                                                         self.ufo.image_rect.centery,
                                                         random.randint(0, 360),
                                                         False))
                self._last_time_ufo_fired = pygame.time.get_ticks()

    def _spawn_ufo(self):
        if self.ufo is None and pygame.time.get_ticks() - self._time_ufo_was_destroyed >= 15000:
            self.ufo = ufo.UFO(random.randint(0, self.height), random.randint(0,1))
            self._last_time_ufo_fired = pygame.time.get_ticks()

    def _update_rocket(self):
        if self.lives >= 1 and self.rocket_destroyed:
            self.rocket.respawn()
            self.lives -= 1
            self.rocket_destroyed = False
        else:
            self.rocket.update(self.size)
            self._rocket_hit_other_obj()
            self._add_supply_capsule()

    def _add_supply_capsule(self):
        if len(self.collectible_objects) < 2 and \
                pygame.time.get_ticks() - self._last_time_capsule_spawned >= self._capsule_timeout:
            if self.rocket.fuel_percent() < 40 or self.rocket.ammo_percent() < 40:
                self._last_time_capsule_spawned = pygame.time.get_ticks()
                self.collectible_objects.add(supply_capsule.SupplyCapsule(random.randint(0, self.size[0]),
                                                                          random.randint(0, self.size[1])))

    def _update_bullets(self):
        far_bullets = []
        for i in range(len(self.active_bullets)):
            if self.active_bullets[i].is_far_enough():
                far_bullets.append(i)
            else:
                self.active_bullets[i].update(self.size)
        self._clear_bullets(far_bullets)
        self._bullet_hit_smth()

    def _update_asteroids(self):
        for aster in self.active_asteroids:
            aster.update(self.size)
        self._aster_hit_smht()

    def _update_ufo(self):
        self._spawn_ufo()
        if self.ufo:
            self.ufo.update(self.size)
            self._ufo_fire()

    def _bullet_hit_smth(self):
        bul_to_destroy = set()
        aster_to_destroy = set()
        for i in range(len(self.active_bullets)):
            bullet_hit = False
            for j in range(len(self.active_asteroids)):
                if self.active_asteroids[j].image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                                    self.active_bullets[i].cur_y):
                    if self.active_bullets[i].rocket_fired:
                        self.rocket.score += 10
                    bul_to_destroy.add(i)
                    aster_to_destroy.add(j)
                    bullet_hit = True
                    break
            if bullet_hit:
                break
            if self.ufo is not None and \
                    self.active_bullets[i].rocket_fired and \
                    self.ufo.image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                     self.active_bullets[i].cur_y):
                self._time_ufo_was_destroyed = pygame.time.get_ticks()
                self.ufo = None
                self.rocket.score += 20
            elif not self.active_bullets[i].rocket_fired:
                if not (self.rocket.is_invincible() or self.rocket_destroyed) and \
                        self.rocket.image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                            self.active_bullets[i].cur_y):
                    self.rocket_destroyed = True
                else:
                    obj_to_del = None
                    for obj in self.collectible_objects:
                        if obj.image_rect.collidepoint(self.active_bullets[i].cur_x,
                                                       self.active_bullets[i].cur_y):
                            bul_to_destroy.add(i)
                            obj_to_del = obj
                            break
                    if obj_to_del:
                        self.collectible_objects.remove(obj_to_del)

        self._clear_bullets(bul_to_destroy)
        self._clear_aster(aster_to_destroy)

    def _aster_hit_smht(self):
        asters_to_del = set()
        for i in range(len(self.active_asteroids)):
            aster = self.active_asteroids[i]
            if self.ufo is not None and \
                    self.ufo.image_rect.colliderect(aster.image_rect):
                self._time_ufo_was_destroyed = pygame.time.get_ticks()
                self.ufo = None
                asters_to_del.add(i)
            elif not (self.rocket.is_invincible() or self.rocket_destroyed) and \
                    self.rocket.image_rect.colliderect(aster.image_rect):
                self.rocket_destroyed = True
                asters_to_del.add(i)
            else:
                obj_to_del = None
                for obj in self.collectible_objects:
                    if aster.image_rect.colliderect(obj.image_rect):
                        asters_to_del.add(i)
                        obj_to_del = obj
                        break
                if obj_to_del:
                    self.collectible_objects.remove(obj_to_del)

        self._clear_aster(asters_to_del, total_destroy=True)

    def _clear_bullets(self, bul_indexes):
        bi = list(bul_indexes)
        bi.sort(reverse=True)
        for i in bi:
            self.active_bullets.pop(i)

    def _clear_aster(self, aster_indexes, total_destroy=False):
        ai = list(aster_indexes)
        ai.sort(reverse=True)
        for i in ai:
            aster = self.active_asteroids.pop(i)
            if not total_destroy and aster.size > 0:
                self.active_asteroids.append(asteroid.Asteroid(aster.size - 1,
                                                               aster.image_rect.x, aster.image_rect.y))
                self.active_asteroids.append(asteroid.Asteroid(aster.size - 1,
                                                               aster.image_rect.x, aster.image_rect.y))

    def _rocket_hit_other_obj(self):
        if self.rocket_destroyed:
            pass
        elif not self.rocket.is_invincible() and\
                self.ufo is not None and self.rocket.image_rect.colliderect(self.ufo.image_rect):
            self.ufo = None
            self.rocket_destroyed = True
        else:
            obj_to_del = None
            for obj in self.collectible_objects:
                if isinstance(obj, supply_capsule.SupplyCapsule)\
                        and self.rocket.image_rect.colliderect(obj.image_rect):
                    self.rocket.resupply(True, True)
                    obj_to_del = obj
                    break
            if obj_to_del:
                self.collectible_objects.remove(obj_to_del)

