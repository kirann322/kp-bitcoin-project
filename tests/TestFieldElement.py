import unittest
import sys
sys.path.append("./")
from src.FieldElement import FieldElement

class TestFieldElement(unittest.TestCase):
    def test_eq(self):
        a = FieldElement(61, 33)
        b = FieldElement(61, 33)
        self.assertEqual(a, b)

    def test_ne(self):
        a = FieldElement(61, 44)
        b = FieldElement(61, 33)
        self.assertNotEqual(a, b)

    def test_add(self):
        a = FieldElement(61, 44)
        b = FieldElement(61, 33)
        c = FieldElement(61, 16)
        self.assertEqual(a + b, c)

        d = FieldElement(61, 17)
        e = FieldElement(61, 42)
        f = FieldElement(61, 49)
        g = FieldElement(61, 47)
        self.assertEqual(d + e + f, g)

    def test_sub(self):
        a = FieldElement(61, 9)
        b = FieldElement(61, 29)
        c = FieldElement(61, 41)
        self.assertEqual(a - b, c)

        d = FieldElement(61, 52)
        e = FieldElement(61, 30)
        f = FieldElement(61, 38)
        g = FieldElement(61, 45)
        self.assertEqual(d - e - f, g)
    
    def test_mul(self):
        a = FieldElement(97, 95)
        b = FieldElement(97, 45)
        c = FieldElement(97, 31)
        d = FieldElement(97, 23)
        self.assertEqual(a * b * c, d)

        e = FieldElement(97, 17)
        f = FieldElement(97, 13)
        g = FieldElement(97, 19)
        h = FieldElement(97, 44)
        i = FieldElement(97, 68)
        self.assertEqual(e * f * g * h, i)
    
    def test_pow(self):
        a = FieldElement(97, 44) ** 7
        b = FieldElement(97, 33) ** 49
        c = FieldElement(97, 95)
        self.assertEqual(a * b, c)
    
    def test_truediv(self):
        a = FieldElement(19, 2)
        b = FieldElement(19, 7)
        c = FieldElement(19, 3)
        self.assertEqual(a / b, c)

        d = FieldElement(19, 7)
        e = FieldElement(19, 5)
        f = FieldElement(19, 9)
        self.assertEqual(d / e, f)

if __name__ == '__main__':
    unittest.main()
