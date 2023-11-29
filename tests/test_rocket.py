import unittest
import rocket
import pygame

pygame.init()
SIZE = (800, 600)
_ = pygame.display.set_mode(SIZE)


class TestRocket(unittest.TestCase):
    def testTurnsWithEnoughFuel(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.turn_right()
        self.assertEqual(rc.rotation_angle, -5)
        rc.rotation_angle = 0
        rc.turn_left()
        self.assertEqual(rc.rotation_angle, 5)

    def testTurnsWithoutEnoughFuel(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.rotation_angle = 0
        rc.fuel = 0.01
        rc.turn_right()
        self.assertEqual(rc.rotation_angle, 0)
        rc.turn_left()
        self.assertEqual(rc.rotation_angle, 0)

    def testSpeedUpWithEnoughFuel(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.speed = 2
        rc.increase_speed()
        self.assertEqual(rc.speed, 2.1)

    def testSpeedUpWithOutEnoughFuel(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.speed = 2
        rc.fuel = 0
        rc.increase_speed()
        self.assertEqual(rc.speed, 2)

    def testMovedCorrectly(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.speed = 1
        rc._moving_angle = 60
        rc.update(SIZE)
        self.assertAlmostEqual(rc.rotated_rect.centerx, 400)
        self.assertEqual(rc.rotated_rect.centery, 299)

    def testFixedOutOfRightBorderCorrectly(self):
        rc = rocket.Rocket(820, 300, hard_mode=True)
        rc.speed = 10
        rc._moving_angle = 0
        rc.update(SIZE)
        self.assertEqual(rc.rotated_rect.right, 0)

    def testFixedOutOfLeftBorderCorrectly(self):
        rc = rocket.Rocket(-50, 300, hard_mode=True)
        rc.speed = 10
        rc._moving_angle = 180
        rc.update(SIZE)
        self.assertEqual(rc.rotated_rect.left, 800)

    def testFixedOutOfUpBorderCorrectly(self):
        rc = rocket.Rocket(400, -50, hard_mode=True)
        rc.speed = 10
        rc._moving_angle = 90
        rc.update(SIZE)
        self.assertEqual(rc.rotated_rect.top, 600)

    def testFixedOutOfDownBorderCorrectly(self):
        rc = rocket.Rocket(450, 650, hard_mode=True)
        rc.speed = 10
        rc._moving_angle = -90
        rc.update(SIZE)
        self.assertEqual(rc.rotated_rect.bottom, 0)

    def testSpeedFade(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.speed = 10
        rc.update(SIZE)
        self.assertEqual(rc.speed, 9.99)

    def testSpeedFadeNotNegative(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.speed = 0
        rc.update(SIZE)
        self.assertEqual(rc.speed, 0)

    def testRespawn(self):
        rc = rocket.Rocket(400, 300, hard_mode=True)
        rc.speed = 10
        rc.update(SIZE)
        rc.respawn()
        self.assertEqual(rc.rotated_rect.centerx, 400)
        self.assertEqual(rc.rotated_rect.centery, 300)

if __name__ == '__main__':
    unittest.main()