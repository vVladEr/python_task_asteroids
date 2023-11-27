import math
import pygame
import random
from gameObject import gameObject, get_angle_in_radians


class Asteroid(gameObject):
    def __init__(self, size, pos_x, pos_y):
        super().__init__()
        self._speed = 0
        self._scale = 0
        self.size = size
        self._set_speed_and_scale(size)
        self.image = pygame.image.load(f"pictures/asteroid{random.randint(1,4)}.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, self._scale)
        self.image_rect = self.image.get_rect(center=(pos_x, pos_y))
        self._moving_angle = random.randint(0, 360)

    def _set_speed_and_scale(self, size):
        self._speed = 2 ** (2-size) + 1
        self._scale = 0.4 + size * 0.3

    def _get_next_frame_coord(self):
        self.image_rect.y -= self._speed * math.sin(get_angle_in_radians(self._moving_angle))
        self.image_rect.x += self._speed * math.cos(get_angle_in_radians(self._moving_angle))

    def _get_angle_in_radians(self):
        return self._moving_angle / 360 * 2 * math.pi

    def _fix_out_of_borders(self, screen_size):
        if self.image_rect.x >= screen_size[0]:
            self.image_rect.x = -self.image.get_rect().size[0]
        elif self.image_rect.right <= 0:
            self.image_rect.x = screen_size[0]
        if self.image_rect.top >= screen_size[1]:
            self.image_rect.top = -self.image.get_rect().size[1]
        elif self.image_rect.bottom <= 0:
            self.image_rect.top = screen_size[1]

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)
