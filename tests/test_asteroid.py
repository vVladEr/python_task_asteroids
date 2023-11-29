import unittest
import asteroid
import pygame

pygame.init()
SIZE = (800, 600)
_ = pygame.display.set_mode(SIZE)


class TestRocket(unittest.TestCase):

    def testMovedCorrectly(self):
        aster = asteroid.Asteroid(0, 400, 300, True, 0)
        aster.update(SIZE)
        self.assertEqual(aster.image_rect.centerx, 405)
        self.assertEqual(aster.image_rect.centery, 300)

    def testFixedOutOfRightBorderCorrectly(self):
        aster = asteroid.Asteroid(0, 850, 300, True, 0)
        aster.update(SIZE)
        self.assertEqual(aster.image_rect.right, 0)

    def testFixedOutOfLeftBorderCorrectly(self):
        aster = asteroid.Asteroid(0, -50, 300, True, 180)
        aster.update(SIZE)
        self.assertEqual(aster.image_rect.left, 800)

    def testFixedOutOfUpBorderCorrectly(self):
        aster = asteroid.Asteroid(0, 400, -50, True, 90)
        aster.update(SIZE)
        self.assertEqual(aster.image_rect.top, 600)

    def testFixedOutOfDownBorderCorrectly(self):
        aster = asteroid.Asteroid(0, 400, 650, True, -90)
        aster.update(SIZE)
        self.assertEqual(aster.image_rect.bottom, 0)


if __name__ == '__main__':
    unittest.main()