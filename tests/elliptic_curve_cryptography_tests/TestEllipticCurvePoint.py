import unittest
from src.elliptic_curve_cryptography.FiniteFieldElement import *
from src.elliptic_curve_cryptography.EllipticCurvePoint import *

class TestEllipticCurvePoint(unittest.TestCase):  
    def test_is_on_curve(self):
        prime = 223
        a = FiniteFieldElement(prime, 0)
        b = FiniteFieldElement(prime, 7)
        valid_points = ((192, 105), (17, 56), (1, 193))
        for x_raw, y_raw in valid_points:
            x = FiniteFieldElement(prime, x_raw)
            y = FiniteFieldElement(prime, y_raw)
            point = EllipticCurvePoint(a, b, x, y)
            self.assertTrue(point.is_on_curve())
        invalid_points = ((200, 119), (42, 99), (35, 56), (37, 74), (25, 50))
        for x_raw, y_raw in invalid_points:
            x = FiniteFieldElement(prime, x_raw)
            y = FiniteFieldElement(prime, y_raw)
            point = EllipticCurvePoint(a, b, x, y)
            self.assertFalse(point.is_on_curve())
        p = (2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1)
        self.assertTrue(
            EllipticCurvePoint(
                FiniteFieldElement(p, 0),
                FiniteFieldElement(p, 7),
                FiniteFieldElement(p, 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798),
                FiniteFieldElement(p, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
            )
        )
    
    def test_is_same_curve(self):
        c1 = EllipticCurvePoint(5, 7, 1, 1)
        c2 = EllipticCurvePoint(7, 7, 1, 1)
        c3 = EllipticCurvePoint(5, 7, -1, -1)
        self.assertFalse(c1.is_same_curve(c2))
        self.assertTrue(c1.is_same_curve(c3))

    def test_eq(self):
        a = EllipticCurvePoint(5, 7, -1, -1)
        b = EllipticCurvePoint(5, 7, -1, -1)
        self.assertEqual(a, b)

    def test_ne(self):
        a = EllipticCurvePoint(5, 7, -1, -1)
        b = EllipticCurvePoint(5, 7, 18, 77)
        self.assertNotEqual(a, b)
    
    def test_add(self):
        prime = 223
        a = FiniteFieldElement(prime, 0)
        b = FiniteFieldElement(prime, 7)
        point1 = [(170, 142), (47, 71), (143, 98), (192, 105), (47, 71), (143, 98)]
        point2 = [(60, 139), (17, 56), (76, 66), (17, 56), (117, 141), (76, 66)]
        point3 = [(220, 181), (215, 68), (47, 71), (170, 142), (60, 139), (47, 71)]
        for idx in range(0, 6, 1):
            p1 = EllipticCurvePoint(a, b, FiniteFieldElement(prime, point1[idx][0]), FiniteFieldElement(prime, point1[idx][1]))
            p2 = EllipticCurvePoint(a, b, FiniteFieldElement(prime, point2[idx][0]), FiniteFieldElement(prime, point2[idx][1]))
            p3 = EllipticCurvePoint(a, b, FiniteFieldElement(prime, point3[idx][0]), FiniteFieldElement(prime, point3[idx][1]))
            self.assertEqual(p1+p2, p3)
    
    def test_mul(self):
        prime = 223
        a = FiniteFieldElement(prime, 0)
        b = FiniteFieldElement(prime, 7)
        point_set = [(192, 105), (143, 98), (47, 71), (47, 71), (47, 71), (47, 71)]
        multiples = [2, 2, 2, 4, 8, 21]
        results = [(49, 71), (64, 168), (36, 111), (194, 51), (116, 55), (None, None)]
        for idx in range(0, 6, 1):
            point = EllipticCurvePoint(a, b, FiniteFieldElement(prime, point_set[idx][0]), FiniteFieldElement(prime, point_set[idx][1])) * multiples[idx]
            self.assertEqual(point, EllipticCurvePoint(a, b, results[idx][0], results[idx][1]))
    
    def test_rmul(self):
        prime = 223
        a = FiniteFieldElement(prime, 0)
        b = FiniteFieldElement(prime, 7)
        point_set = [(192, 105), (143, 98), (47, 71), (47, 71), (47, 71), (47, 71)]
        multiples = [2, 2, 2, 4, 8, 21]
        results = [(49, 71), (64, 168), (36, 111), (194, 51), (116, 55), (None, None)]
        for idx in range(0, 6, 1):
            point = multiples[idx] * EllipticCurvePoint(a, b, FiniteFieldElement(prime, point_set[idx][0]), FiniteFieldElement(prime, point_set[idx][1]))
            self.assertEqual(point, EllipticCurvePoint(a, b, results[idx][0], results[idx][1]))

if __name__ == '__main__':
    unittest.main()
