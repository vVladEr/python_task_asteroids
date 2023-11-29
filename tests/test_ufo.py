import unittest
import ufo
import pygame

pygame.init()
SIZE = (800, 600)
_ = pygame.display.set_mode(SIZE)


class TestRocket(unittest.TestCase):

    def testMovedCorrectly(self):
        u = ufo.UFO(400, 0)
        u.update(SIZE)
        self.assertEqual(u.image_rect.centerx, 3)
        self.assertEqual(u.image_rect.centery, 400)

    def testFixedOutOfRightBorderCorrectly(self):
        u = ufo.UFO(400, 0, 850)
        u.update(SIZE)
        self.assertEqual(u.image_rect.right, 0)

    def testFixedOutOfLeftBorderCorrectly(self):
        u = ufo.UFO(400, 1, -50)
        u.update(SIZE)
        self.assertEqual(u.image_rect.left, 800)


if __name__ == '__main__':
    unittest.main()