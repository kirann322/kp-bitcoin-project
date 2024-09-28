import unittest
import sys
sys.path.append("./")
from src.EllipticCurvePoint import EllipticCurvePoint
from src.FieldElement import FieldElement

class TestEllipticCurvePoint(unittest.TestCase):
    def test_init(self):
        a = EllipticCurvePoint(5, 7, -1, -1)
        self.assertIsInstance(a, EllipticCurvePoint)
        with self.assertRaises(ValueError):
            b = EllipticCurvePoint(5, 7, -1, -2)

    def test_eq(self):
        a = EllipticCurvePoint(5, 7, -1, -1)
        b = EllipticCurvePoint(5, 7, -1, -1)
        self.assertEqual(a, b)

    def test_ne(self):
        a = EllipticCurvePoint(5, 7, -1, -1)
        b = EllipticCurvePoint(5, 7, 18, 77)
        self.assertNotEqual(a, b)
    
    def test_elliptic_curve_over_finite_field(self):
        prime = 223
        a = FieldElement(prime, 0)
        b = FieldElement(prime, 7)
        valid_points = [(192, 105), (17, 56), (1, 193)]
        invalid_points = [(200, 119), (42, 99)]
        for x, y in valid_points:
            x_field = FieldElement(prime, x)
            y_field = FieldElement(prime, y)
            new_point = EllipticCurvePoint(a, b, x_field, y_field)
        for x, y in invalid_points:
            x_field = FieldElement(prime, x)
            y_field = FieldElement(prime, y)
            with self.assertRaises(ValueError):
                new_point = EllipticCurvePoint(a, b, x_field, y_field)

if __name__ == '__main__':
    unittest.main()
