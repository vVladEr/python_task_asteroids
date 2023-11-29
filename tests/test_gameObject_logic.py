import unittest
import bullet
import gameObjectsLogic
import supply_capsule
import ufo
from asteroid import Asteroid
import pygame


pygame.init()
SIZE = (800, 600)
_ = pygame.display.set_mode(SIZE)


class TestGameObjectLogic(unittest.TestCase):

    def testCheckOriginState(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        objects = list(game_objects.get_all_objects())
        self.assertEqual(1, len(objects))
        self.assertIsInstance(objects[0], Asteroid)

    def testFire(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_bullets.clear()
        pygame.time.wait(151)
        game_objects.fire()
        self.assertEqual(1, len(game_objects.active_bullets))

    def testFireWithoutAmmo(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_bullets.clear()
        game_objects.rocket.ammo = 0
        pygame.time.wait(151)
        game_objects.fire()
        self.assertEqual(0, len(game_objects.active_bullets))

    def testRestartLevel(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_asteroids.clear()
        game_objects._level_restart()
        self.assertEqual(3, len(game_objects.active_asteroids))

    def testSpawnUfo(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_asteroids.clear()
        game_objects._time_ufo_was_destroyed = -150000
        game_objects._spawn_ufo()
        self.assertIsNotNone(game_objects.ufo)

    def testUfoFire(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_bullets.clear()
        game_objects.ufo = ufo.UFO(300, 0)
        game_objects._last_time_ufo_fired = -1000000
        game_objects._ufo_fire()
        self.assertEqual(1, len(game_objects.active_bullets))
        self.assertEqual(False, game_objects.active_bullets[0].rocket_fired)

    def testSupplyCapsuleSpawn(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects._capsule_timeout = -1
        game_objects.rocket.fuel = 0
        game_objects._add_supply_capsule()
        self.assertEqual(1, len(game_objects.collectible_objects))

    def testDelFarBullets(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_asteroids.clear()
        game_objects.active_bullets.append(bullet.Bullet(100, 100, 0, True))
        game_objects.active_bullets.append(bullet.Bullet(100, 120, 0, True))
        pygame.time.wait(751)
        game_objects._update_bullets()
        self.assertEqual(0, len(game_objects.active_bullets))

    def testRocketBulletHitAster(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_asteroids.clear()
        game_objects.active_bullets.append(bullet.Bullet(100, 100, 0, True))
        game_objects.active_asteroids.append(Asteroid(2, 100, 100))
        game_objects._bullet_hit_smth()
        self.assertEqual(0, len(game_objects.active_bullets))
        self.assertEqual(2, len(game_objects.active_asteroids))
        self.assertEqual(10, game_objects.rocket.score)

    def testUfoBulletHitAster(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_asteroids.clear()
        game_objects.active_bullets.append(bullet.Bullet(100, 100, 0, False))
        game_objects.active_asteroids.append(Asteroid(0, 100, 100))
        game_objects._bullet_hit_smth()
        self.assertEqual(0, len(game_objects.active_bullets))
        self.assertEqual(0, len(game_objects.active_asteroids))
        self.assertEqual(0, game_objects.rocket.score)

    def testUfoHitAster(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_asteroids.clear()
        game_objects.ufo = ufo.UFO(100, 0, x=100)
        game_objects.active_asteroids.append(Asteroid(2, 100, 100))
        game_objects._aster_hit_smht()
        self.assertIsNone(game_objects.ufo)
        self.assertEqual(0, len(game_objects.active_asteroids))

    def testAsterDestroyRocket(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_asteroids.clear()
        game_objects.active_asteroids.append(Asteroid(2, 400, 300))
        game_objects._aster_hit_smht()
        self.assertEqual(False, game_objects.rocket_destroyed)
        self.assertEqual(1, len(game_objects.active_asteroids))
        game_objects.rocket._invincible_time = -1
        game_objects._aster_hit_smht()
        self.assertEqual(True, game_objects.rocket_destroyed)
        self.assertEqual(0, len(game_objects.active_asteroids))

    def testRocketBulDestroyUFO(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.ufo = ufo.UFO(100, 1, x=100)
        game_objects.active_bullets.append(bullet.Bullet(100, 100, 0, True))
        game_objects._bullet_hit_smth()
        self.assertEqual(20, game_objects.rocket.score)
        self.assertIsNone(game_objects.ufo)

    def testUfoBulDestroyRocket(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.active_bullets.append(bullet.Bullet(400, 300, 0, False))
        game_objects._bullet_hit_smth()
        self.assertEqual(False, game_objects.rocket_destroyed)
        game_objects.rocket._invincible_time = -1
        game_objects._bullet_hit_smth()
        self.assertEqual(True, game_objects.rocket_destroyed)

    def testRocketCollectSupply(self):
        game_objects = gameObjectsLogic.GameObjectsLogic(SIZE, hard_mode=True)
        game_objects.collectible_objects.add(supply_capsule.SupplyCapsule(400, 300))
        game_objects.rocket.fuel = 0
        game_objects.rocket.ammo = 1
        game_objects._rocket_hit_other_obj()
        self.assertEqual(100, game_objects.rocket.fuel_percent())
        self.assertEqual(100, game_objects.rocket.ammo_percent())


if __name__ == '__main__':
    unittest.main()