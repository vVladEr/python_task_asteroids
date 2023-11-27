import math
import pygame
import random

from gameObject import gameObject, get_angle_in_radians


class UFO(gameObject):
    def __init__(self, height):
        super().__init__()
        self._scale = 0
        self._scale = 0.4 + random.randint(0, 2) * 0.3
        self._speed = 3
        self.image = pygame.image.load(f"pictures/ufo.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, self._scale)
        self.image_rect = self.image.get_rect(center=(0, random.randint(0, height)))
        self._moving_angle = random.randint(0, 1) * 180

    def _get_next_frame_coord(self):
        self.image_rect.y -= self._speed * math.sin(get_angle_in_radians(self._moving_angle))
        self.image_rect.x += self._speed * math.cos(get_angle_in_radians(self._moving_angle))

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
