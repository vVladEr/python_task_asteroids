import math


def get_angle_in_radians(moving_angle):
    return moving_angle / 360 * 2 * math.pi


class gameObject:

    def __init__(self):
        pass

    def draw(self, screen):
        pass

    def _fix_out_of_borders(self, screen_size):
        pass

    def update(self, screen_size):
        self._get_next_frame_coord()
        self._fix_out_of_borders(screen_size)

    def _get_next_frame_coord(self):
        pass
