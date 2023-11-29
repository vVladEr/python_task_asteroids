import unittest
import bullet
import pygame

pygame.init()
SIZE = (800, 600)
_ = pygame.display.set_mode(SIZE)


class TestRocket(unittest.TestCase):

    def testMovedCorrectly(self):
        bl = bullet.Bullet(400, 300, 0, True)
        bl.update(SIZE)
        self.assertEqual(bl.cur_x, 415)
        self.assertEqual(bl.cur_y, 300)

    def testFixedOutOfRightBorderCorrectly(self):
        bl = bullet.Bullet(800, 300, 0, True)
        bl.update(SIZE)
        self.assertEqual(bl.cur_x, 0)

    def testFixedOutOfLeftBorderCorrectly(self):
        bl = bullet.Bullet(0, 300, 180, True)
        bl.update(SIZE)
        self.assertEqual(bl.cur_x, 800)

    def testFixedOutOfUpBorderCorrectly(self):
        bl = bullet.Bullet(400, 0, 90, True)
        bl.update(SIZE)
        self.assertEqual(bl.cur_y, 600)

    def testFixedOutOfDownBorderCorrectly(self):
        bl = bullet.Bullet(400, 600, -90, True)
        bl.update(SIZE)
        self.assertEqual(bl.cur_y, 0)

    def testIsFarEnough(self):
        bl = bullet.Bullet(400, 300, 0, True)
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start <= 3001:
            pass
        self.assertEqual(True, bl.is_far_enough())

if __name__ == '__main__':
    unittest.main()