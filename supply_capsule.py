import pygame
import random

from gameObject import gameObject, get_path_to_image


class SupplyCapsule(gameObject):
    def __init__(self, x, y):
        super().__init__()
        c = get_path_to_image()
        self.image = pygame.image.load(f"{'../'*c}pictures/resupply_capsule.png").convert_alpha()
        self.image_rect = self.image.get_rect(center=(x,y))

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)
