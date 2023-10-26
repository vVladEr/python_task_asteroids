import math
import pygame
import random

width = 800
height = 600


class Asteroid:
    def __init__(self, screen, size, pos_x, pos_y):
        self._screen = screen
        self._speed = 0
        self._scale = 0
        self.size = size
        self._set_speed_and_scale(size)
        self.image = pygame.image.load("rocket.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, self._scale)
        self.image_rect = self.image.get_rect(center=(pos_x, pos_y))
        self._moving_angle = random.randint(0, 360)

    def _set_speed_and_scale(self, size):
        self._speed = 2 ** (2-size)
        self._scale = 2 ** -(2-size)

    def update(self):
        self.image_rect.y -= self._speed * math.sin(self._get_angle_in_radians())
        self.image_rect.x += self._speed * math.cos(self._get_angle_in_radians())
        self._fix_out_of_borders()
        self._screen.blit(self.image, self.image_rect)

    def _get_angle_in_radians(self):
        return self._moving_angle / 360 * 2 * math.pi

    def _fix_out_of_borders(self):
        if self.image_rect.x >= width:
            self.image_rect.x = -self.image.get_rect().size[0]
        elif self.image_rect.right <= 0:
            self.image_rect.x = width
        if self.image_rect.top >= height:
            self.image_rect.top = -self.image.get_rect().size[1]
        elif self.image_rect.bottom <= 0:
            self.image_rect.top = height
