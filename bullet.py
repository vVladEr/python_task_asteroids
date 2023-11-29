import pygame
import math

from gameObject import gameObject, get_angle_in_radians

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


class Bullet(gameObject):
    def __init__(self, x, y, moving_angle, rocket_fired):
        super().__init__()
        self.spawn_point_x = x
        self.spawn_point_y = y
        self.cur_x = x
        self.cur_y = y
        self.moving_angle = moving_angle
        self.speed = 15
        self.max_distance = 600
        self._radius = 4
        self._max_time_to_live = 750
        self._fire_time = pygame.time.get_ticks()
        self.rocket_fired = rocket_fired

    def _get_next_frame_coord(self):
        self.cur_x += self.speed * math.cos(get_angle_in_radians(self.moving_angle))
        self.cur_y -= self.speed * math.sin(get_angle_in_radians(self.moving_angle))

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.cur_x, self.cur_y), self._radius)

    def is_far_enough(self):
        return (pygame.time.get_ticks() - self._fire_time) > self._max_time_to_live

    def _fix_out_of_borders(self, screen_size):
        if self.cur_x >= screen_size[0]:
            self.cur_x = 0
        elif self.cur_x <= 0:
            self.cur_x = screen_size[0]
        if self.cur_y >= screen_size[1]:
            self.cur_y = 0
        elif self.cur_y <= 0:
            self.cur_y = screen_size[1]
