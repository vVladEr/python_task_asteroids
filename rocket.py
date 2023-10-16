
import math
import pygame


width = 800
height = 600


class Rocket:
    def __init__(self, start_x, start_y):
        self.speed = 0
        self.rotation_angle = 0
        self.image = pygame.image.load("arrow.png").convert_alpha()
        self.rotated_rect = self.image.get_rect(center=(start_x, start_y))
        self.image_rect = self.image.get_rect(center=(start_x, start_y))
        self.rotated_image = self.image

    def turn_right(self):
        self.rotation_angle -= 2
        self.rotate_rocket_image()

    def turn_left(self):
        self.rotation_angle += 2
        self.rotate_rocket_image()

    def rotate_rocket_image(self):
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.image_rect.center)

    def increase_speed(self):
        self.speed = min(self.speed + 0.1,  3)

    def fade_speed(self):
        self.speed = max(self.speed - 0.03, 0)

    def get_next_frame_coordinates(self):
        self.rotated_rect.x += self.speed * math.cos(self._get_angle_in_radians())
        self.image_rect.x += self.speed * math.cos(self._get_angle_in_radians())
        self.rotated_rect.y -= self.speed * math.sin(self._get_angle_in_radians())
        self.image_rect.y -= self.speed * math.sin(self._get_angle_in_radians())
        self.fade_speed()

    def _get_angle_in_radians(self):
        return self.rotation_angle / 360 * 2 * math.pi
