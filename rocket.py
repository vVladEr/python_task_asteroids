import math
import pygame

from gameObject import gameObject, get_angle_in_radians, get_path_to_image


class Rocket(gameObject):
    def __init__(self, start_x, start_y, hard_mode=False):
        super().__init__()
        self.speed = 0
        self._moving_angle = 0
        self.rotation_angle = 0
        c = get_path_to_image()
        self.image = pygame.image.load(f"{'../' * c}pictures/rocket.png").convert_alpha()
        self.rotated_rect = self.image.get_rect(center=(start_x, start_y))
        self.image_rect = self.image.get_rect(center=(start_x, start_y))
        self.rotated_image = self.image
        self.score = 0
        self._start_x = start_x
        self._start_y = start_y
        self._invincible_time_start = pygame.time.get_ticks()
        self._invincible_time = 2000
        self.hard_mode = hard_mode
        self.fuel_to_rotate = 0
        self.fuel_to_speed_up = 0
        if hard_mode:
            self.fuel_to_rotate = 0.1
            self.fuel_to_speed_up = 0.5
            self.max_ammo = 100
            self.max_fuel = 1000
            self.ammo = self.max_ammo
            self.fuel = self.max_fuel

    def _is_enough_fuel(self, fuel_to_spend):
        if self.hard_mode:
            if self.fuel >= fuel_to_spend:
                self.fuel -= fuel_to_spend
                return True
            return False
        return True

    def turn_right(self):
        if self._is_enough_fuel(self.fuel_to_rotate):
            self.rotation_angle -= 5
            self.rotate_rocket_image()

    def turn_left(self):
        if self._is_enough_fuel(self.fuel_to_rotate):
            self.rotation_angle += 5
            self.rotate_rocket_image()

    def rotate_rocket_image(self):
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.image_rect.center)

    def increase_speed(self):
        if self._is_enough_fuel(self.fuel_to_speed_up):
            self.speed = min(self.speed + 0.1, 7)
            self._moving_angle = self.rotation_angle

    def _fade_speed(self):
        self.speed = max(self.speed - 0.01, 0)
        if self.speed == 0:
            self._moving_angle = self.rotation_angle

    def update(self, screen_size):
        super().update(screen_size)
        self._fade_speed()

    def _get_next_frame_coord(self):
        self.rotated_rect.x += self.speed * math.cos(get_angle_in_radians(self._moving_angle))
        self.image_rect.x += self.speed * math.cos(get_angle_in_radians(self._moving_angle))
        self.rotated_rect.y -= self.speed * math.sin(get_angle_in_radians(self._moving_angle))
        self.image_rect.y -= self.speed * math.sin(get_angle_in_radians(self._moving_angle))

    def _fix_out_of_borders(self, screen_size):
        if self.image_rect.x >= screen_size[0]:
            self.image_rect.x = -self.image.get_rect().size[0]
            self.rotated_rect.x = -self.rotated_image.get_rect().size[0]
        elif self.image_rect.right <= 0:
            self.image_rect.x = screen_size[0]
            self.rotated_rect.x = screen_size[0]
        if self.image_rect.top >= screen_size[1]:
            self.image_rect.top = -self.image.get_rect().size[1]
            self.rotated_rect.top = -self.rotated_image.get_rect().size[1]
        elif self.image_rect.bottom <= 0:
            self.image_rect.top = screen_size[1]
            self.rotated_rect.top = screen_size[1]

    def respawn(self):
        self.rotated_rect = self.image.get_rect(center=(self._start_x, self._start_y))
        self.image_rect = self.image.get_rect(center=(self._start_x, self._start_y))
        self._moving_angle = 0
        self.rotation_angle = 0
        self.rotate_rocket_image()
        self.speed = 0
        self.make_invincible()
        self.resupply(ammo=True, fuel=True)

    def is_invincible(self):
        return (pygame.time.get_ticks() - self._invincible_time_start) <= self._invincible_time

    def make_invincible(self):
        self._invincible_time_start = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rotated_rect)

    def fire(self):
        if self.hard_mode:
            self.ammo -= 1

    def is_enough_ammo(self):
        return self.ammo > 0

    def resupply(self, ammo=False, fuel=False):
        if ammo:
            self.ammo = self.max_ammo
        if fuel:
            self.fuel = self.max_fuel

    def fuel_percent(self):
        return (self.fuel / self.max_fuel) * 100

    def ammo_percent(self):
        return (self.ammo / self.max_ammo) * 100
