import bullet
import math
import pygame


width = 800
height = 600


class Rocket:
    def __init__(self, start_x, start_y):
        self.speed = 0
        self.moving_angle = 0
        self.rotation_angle = 0
        self.image = pygame.image.load("rocket.png").convert_alpha()
        self.rotated_rect = self.image.get_rect(center=(start_x, start_y))
        self.image_rect = self.image.get_rect(center=(start_x, start_y))
        self.rotated_image = self.image
        self.active_bullets = []

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
        self.speed = min(self.speed + 0.1,  5)
        if self.moving_angle > self.rotation_angle:
            self.moving_angle = max(self.rotation_angle, self.moving_angle - 3)
        elif self.moving_angle < self.rotation_angle:
            self.moving_angle = min(self.rotation_angle, self.moving_angle + 3)

    def fade_speed(self):
        self.speed = max(self.speed - 0.01, 0)

    def get_next_frame_coordinates(self):
        self.rotated_rect.x += self.speed * math.cos(self._get_angle_in_radians())
        self.image_rect.x += self.speed * math.cos(self._get_angle_in_radians())
        self.rotated_rect.y -= self.speed * math.sin(self._get_angle_in_radians())
        self.image_rect.y -= self.speed * math.sin(self._get_angle_in_radians())
        self._fix_out_of_borders()
        self.fade_speed()
#        self.update_bullets()

    def _get_angle_in_radians(self):
        return self.moving_angle / 360 * 2 * math.pi

    def _fix_out_of_borders(self):
        if self.image_rect.x >= width:
            self.image_rect.x = -self.image.get_rect().size[0]
            self.rotated_rect.x = -self.rotated_image.get_rect().size[0]
        elif self.image_rect.right <= 0:
            self.image_rect.x = width
            self.rotated_rect.x = width
        if self.image_rect.top >= height:
            self.image_rect.top = -self.image.get_rect().size[1]
            self.rotated_rect.top = -self.rotated_image.get_rect().size[1]
        elif self.image_rect.bottom <= 0:
            self.image_rect.top = height
            self.rotated_rect.top = height

    def fire(self):
        if len(self.active_bullets) < 5:
            self.active_bullets.append(bullet.Bullet(self.rotated_rect.centerx,
                                                     self.rotated_rect.centery, self.rotation_angle))

    def update_bullets(self):
        for i in range(len(self.active_bullets)):
            if self.active_bullets[i].is_far_enough():
                del self.active_bullets[i]
            else:
                self.active_bullets[i].update()
