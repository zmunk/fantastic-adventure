import unittest
import complete_cube as cc

class TestVector2D(unittest.TestCase):
    def test_sub(self):
        v1 = cc.Vector2D(3, 5)
        v2 = cc.Vector2D(4, 8)
        self.assertEqual(v1, v2, Vector(-1, -3))

