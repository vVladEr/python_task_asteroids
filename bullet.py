import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def _get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


class Bullet:
    def __init__(self, x, y, moving_angle, screen_size, rocket_fired):
        self.spawn_point_x = x
        self.spawn_point_y = y
        self.cur_x = x
        self.cur_y = y
        self.moving_angle = moving_angle
        self.speed = 10
        self.max_distance = 600
        self._radius = 4
        self._cross_top = False
        self._cross_right = False
        self._cross_bottom = False
        self._cross_left = False
        self._screen_size = screen_size
        self.rocket_fired = rocket_fired

    def update(self, screen):
        self.cur_x += self.speed * math.cos(self._get_angle_in_radians())
        self.cur_y -= self.speed * math.sin(self._get_angle_in_radians())
        self._fix_out_of_borders()
        pygame.draw.circle(screen, WHITE, (self.cur_x, self.cur_y), self._radius)

    def is_far_enough(self):
        temp_x = self.cur_x
        temp_y = self.cur_y
        if self._cross_top:
            temp_y = -(self._screen_size[1] - temp_y)
        elif self._cross_bottom:
            temp_y += self._screen_size[1]
        if self._cross_right:
            temp_x += self._screen_size[0]
        elif self._cross_left:
            temp_x = -(self._screen_size[0] - temp_x)
        return _get_distance(temp_x,
                             temp_y,
                             self.spawn_point_x, self.spawn_point_y) >= self.max_distance

    def _get_angle_in_radians(self):
        return self.moving_angle / 360 * 2 * math.pi

    def _fix_out_of_borders(self):
        if self.cur_x >= self._screen_size[0]:
            self.cur_x = 0
            self._cross_right = True
        elif self.cur_x <= 0:
            self.cur_x = self._screen_size[0]
            self._cross_left = True
        if self.cur_y >= self._screen_size[1]:
            self.cur_y = 0
            self._cross_bottom = True
        elif self.cur_y <= 0:
            self.cur_y = self._screen_size[1]
            self._cross_top = True
