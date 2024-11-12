import unittest
from src.elliptic_curve_cryptography.FiniteFieldElement import *

class TestFiniteFieldElement(unittest.TestCase):
    def test_eq(self):
        a = FiniteFieldElement(61, 33)
        b = FiniteFieldElement(61, 33)
        self.assertEqual(a, b)

    def test_ne(self):
        a = FiniteFieldElement(61, 44)
        b = FiniteFieldElement(61, 33)
        self.assertNotEqual(a, b)

    def test_add(self):
        a = FiniteFieldElement(61, 44)
        b = FiniteFieldElement(61, 33)
        c = FiniteFieldElement(61, 16)
        self.assertEqual(a + b, c)

        d = FiniteFieldElement(61, 17)
        e = FiniteFieldElement(61, 42)
        f = FiniteFieldElement(61, 49)
        g = FiniteFieldElement(61, 47)
        self.assertEqual(d + e + f, g)

    def test_sub(self):
        a = FiniteFieldElement(61, 9)
        b = FiniteFieldElement(61, 29)
        c = FiniteFieldElement(61, 41)
        self.assertEqual(a - b, c)

        d = FiniteFieldElement(61, 52)
        e = FiniteFieldElement(61, 30)
        f = FiniteFieldElement(61, 38)
        g = FiniteFieldElement(61, 45)
        self.assertEqual(d - e - f, g)
    
    def test_mul(self):
        a = FiniteFieldElement(97, 95)
        b = FiniteFieldElement(97, 45)
        c = FiniteFieldElement(97, 31)
        d = FiniteFieldElement(97, 23)
        self.assertEqual(a * b * c, d)

        e = FiniteFieldElement(97, 17)
        f = FiniteFieldElement(97, 13)
        g = FiniteFieldElement(97, 19)
        h = FiniteFieldElement(97, 44)
        i = FiniteFieldElement(97, 68)
        self.assertEqual(e * f * g * h, i)
    
    def test_pow(self):
        a = FiniteFieldElement(97, 44) ** 7
        b = FiniteFieldElement(97, 33) ** 49
        c = FiniteFieldElement(97, 95)
        self.assertEqual(a * b, c)
    
    def test_truediv(self):
        a = FiniteFieldElement(19, 2)
        b = FiniteFieldElement(19, 7)
        c = FiniteFieldElement(19, 3)
        self.assertEqual(a / b, c)

        d = FiniteFieldElement(19, 7)
        e = FiniteFieldElement(19, 5)
        f = FiniteFieldElement(19, 9)
        self.assertEqual(d / e, f)

if __name__ == '__main__':
    unittest.main()
