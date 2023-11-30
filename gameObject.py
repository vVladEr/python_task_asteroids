import math
import pathlib


def get_angle_in_radians(moving_angle):
    return moving_angle / 360 * 2 * math.pi


def get_path_to_image(name):
    a = pathlib.Path.cwd().parts
    counter = 0
    for i in range(len(a)-1, -1, -1):
        if a[i] == "python_task_asteroids":
            break
        else:
            counter += 1
    return f"{'../'*counter}pictures/{name}"


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
