import math
import pygame

from gameObject import gameObject, get_angle_in_radians


class Rocket(gameObject):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.speed = 0
        self._moving_angle = 0
        self.rotation_angle = 0
        self.image = pygame.image.load("pictures/rocket.png").convert_alpha()
        self.rotated_rect = self.image.get_rect(center=(start_x, start_y))
        self.image_rect = self.image.get_rect(center=(start_x, start_y))
        self.rotated_image = self.image
        self.active_bullets = []
        self.score = 0
        self._start_x = start_x
        self._start_y = start_y
        self._invincible_time_start = pygame.time.get_ticks()
        self._invincible_time = 2000

    def turn_right(self):
        self.rotation_angle -= 5
        self.rotate_rocket_image()

    def turn_left(self):
        self.rotation_angle += 5
        self.rotate_rocket_image()

    def rotate_rocket_image(self):
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.image_rect.center)

    def increase_speed(self):
        self.speed = min(self.speed + 0.1, 7)
        if self._moving_angle > self.rotation_angle:
            self._moving_angle = max(self.rotation_angle, self._moving_angle - 10)
        elif self._moving_angle < self.rotation_angle:
            self._moving_angle = min(self.rotation_angle, self._moving_angle + 10)

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

    def is_invincible(self):
        return (pygame.time.get_ticks() - self._invincible_time_start) <= self._invincible_time

    def make_invincible(self):
        self._invincible_time_start = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rotated_rect)