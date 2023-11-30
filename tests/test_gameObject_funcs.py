import math

import gameObject
import unittest

NAMES = ["ammo.png", "rocket.png", "asteroids.png"]
ANGlES = {0: 0,
          60: math.pi / 3,
          -60: -math.pi / 3,
          180: math.pi,
          360: 2 * math.pi
          }


class TestGameObjectFuncs(unittest.TestCase):

    def testConvertDegreeInRadians(self):
        for pair in ANGlES.items():
            angle = gameObject.get_angle_in_radians(pair[0])
            self.assertEqual(pair[1], angle)


