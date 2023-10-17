import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def _get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


class Bullet:
    def __init__(self, x, y, moving_angle):
        self.spawn_point_x = x
        self.spawn_point_y = y
        self.cur_x = x
        self.cur_y = y
        self.moving_angle = moving_angle
        self.speed = 7
        self.max_distance = 40
        self._radius = 1

    def update(self, screen):
        pygame.draw.circle(screen, BLACK, (self.cur_x, self.cur_y), self._radius)
        self.cur_x += self.speed * math.cos(self._get_angle_in_radians())
        self.cur_y -= self.speed * math.sin(self._get_angle_in_radians())
        pygame.draw.circle(screen, WHITE, (self.cur_x, self.cur_y), self._radius)

    def is_far_enough(self):
        return _get_distance(self.cur_x, self.cur_y, self.spawn_point_x, self.spawn_point_y) >= self.max_distance

    def _get_angle_in_radians(self):
        return self.moving_angle / 360 * 2 * math.pi


