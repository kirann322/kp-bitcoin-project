from __future__ import annotations

class EllipticCurvePoint:
    def __init__(self, a: int, b: int, x: int, y: int):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        """
        if self.y**2 != self.x**3 + a*x + b and not(x is None and y is None):
            error = f"({x}, {y}) is not on the curve"
            raise ValueError(error)
        """
        """
        if 4 * (a**3) + 27 * (b**2) == 0:
            error = f"a = {a} and b = {b} creates a curve with singularities, this is not allowed"
            raise ValueError(error)
        """
    
    def __repr__(self) -> str:
        return f"Elliptic Curve y^2 = x^3 + {self.a}*x + {self.b} with point ({self.x}, {self.y})"
    
    def __eq__(self, point: EllipticCurvePoint) -> bool:
        x_eq = self.x == point.x
        y_eq = self.y == point.y
        a_eq = self.a == point.a
        b_eq = self.b == point.b
        return (x_eq and y_eq and a_eq and b_eq)
    
    def __ne__(self, point: EllipticCurvePoint) -> bool:
        x_ne = self.x != point.x
        y_ne = self.y != point.y
        a_ne = self.a != point.a
        b_ne = self.b != point.b
        return (x_ne or y_ne or a_ne or b_ne)
    
    def __add__(self, point) -> EllipticCurvePoint:
        if self.a != point.a or self.b != point.b:
            error = "The points are not on the same elliptic curve"
            raise ValueError(error)
        
        if self.x is None and self.y is None:
            return point
        if point.x is None and point.y is None:
            return point
        
        if (self.x == point.x) and (self.y != point.y or self.y == 0 or point.y == 0):
            return EllipticCurvePoint(self.a, self.b, None, None)
        elif self == point:
            slope = (3 * (self.x**2) + self.a) / (2 * self.y)
            x_3 = slope**2 - self.x - point.x
            y_3 = slope * (self.x - x_3) - self.y
        else:
            slope = (point.y - self.y) / (point.x - self.x)
            x_3 = slope**2 - self.x - point.x
            y_3 = slope * (self.x - x_3) - self.y

        return EllipticCurvePoint(self.a, self.b, x_3, y_3)
    
    def __mul__(self, other):
        if isinstance(other, int) and other >= 0:
            current_term = EllipticCurvePoint(self.a, self.b, self.x, self.y)
            solution = EllipticCurvePoint(self.a, self.b, None, None)
            while other:
                if other & 1:
                    solution += current_term
                current_term += current_term
                other = other >> 1
            return solution
        else:
            error = "Incompatible type scalar multiplying with an EllipticCurvePoint"
            raise TypeError(error)
    
    def __rmul__(self, other):
        if isinstance(other, int) and other >= 0:
            current_term = EllipticCurvePoint(self.a, self.b, self.x, self.y)
            solution = EllipticCurvePoint(self.a, self.b, None, None)
            while other:
                if other & 1:
                    solution += current_term
                current_term += current_term
                other = other >> 1
            return solution
        else:
            error = "Incompatible type scalar multiplying with an EllipticCurvePoint"
            raise TypeError(error)
