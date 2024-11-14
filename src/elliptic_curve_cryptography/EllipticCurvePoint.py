from __future__ import annotations

class EllipticCurvePoint:
    def __init__(self, a: int, b: int, x: int, y: int):
        """Instantiates an elliptic curve point of the form y^2 = x^3 + ax + b if the curve is non singular by checking if the discriminant is zero"""
        if (4*(a**3) + 27*(b**2)) == 0:
            error = f"a = {a} and b = {b} creates a curve which is singular and this cannot be used for cryptography"
            raise ValueError(error)
        self.a = a
        self.b = b
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        """Returns string representation of EllipticCurvePoint"""
        return f"Elliptic Curve y^2 = x^3 + {self.a}*x + {self.b} with point ({self.x}, {self.y})"
    
    def __eq__(self, other: EllipticCurvePoint) -> bool:
        """Checks equality of EllipticCurvePoint with other objects"""
        if isinstance(other, EllipticCurvePoint):
            x_eq = (self.x == other.x)
            y_eq = (self.y == other.y)
            a_eq = (self.a == other.a)
            b_eq = (self.b == other.b)
            return (x_eq and y_eq and a_eq and b_eq)
        else:
            error = "Incompatible type making equality comparison to a EllipticCurvePoint"
            raise TypeError(error)
    
    def __ne__(self, other: EllipticCurvePoint) -> bool:
        """Checks non equality of EllipticCurvePoint with other objects"""
        if isinstance(other, EllipticCurvePoint):
            x_ne = (self.x != other.x)
            y_ne = (self.y != other.y)
            a_ne = (self.a != other.a)
            b_ne = (self.b != other.b)
            return (x_ne or y_ne or a_ne or b_ne)
        else:
            error = "Incompatible type making equality comparison to a EllipticCurvePoint"
            raise TypeError(error)
    
    def __add__(self, other: EllipticCurvePoint) -> EllipticCurvePoint:
        """Defines point addition for EllipticCurvePoint"""
        # case 0: validate points
        if not isinstance(other, EllipticCurvePoint):
            error = "EllipticCurvePoint cannot be added to another object"
            return ValueError(error)
        if not self.is_same_curve(other):
            error = "The points are not on the same elliptic curve since the a and b parameters do not match"
            raise ValueError(error)
        # case 1 identity - the point at infinity is being added to any other point, sum will be the non identity point
        if self.x is None and self.y is None:
            return other
        if other.x is None and other.y is None:
            return self
        # case 2 additive identity - vertical line with 2 intersection points being added together, sum of the points will be the identity point at infinity
        if self.x == other.x and self.y != other.y:
            return EllipticCurvePoint(self.a, self.b, None, None)
        # case 3 sloped line 3 intersections - line that intersects at 3 points, 2 of the points are being added to find the reflection of the 3rd point
        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x_3 = slope**2 - self.x - other.x
            y_3 = slope * (self.x - x_3) - self.y
            return EllipticCurvePoint(self.a, self.b, x_3, y_3)
        # case 4 vertical tangent - vertical line that intersects once at a tangent, 2 overlapping points where one points y value is 0, sums to the identity point
        if self == other and (self.y == 0 or other.y == 0):
            return EllipticCurvePoint(self.a, self.b, None, None)
        # case 5 sloped line with tangent point - sloped line with 1 tangent intersection, 2 points are equal at the tangent, summing requires finding the final intersection point
        if self == other:
            slope = (3 * (self.x**2) + self.a) / (2 * self.y)
            x_3 = slope**2 - self.x - other.x
            y_3 = slope * (self.x - x_3) - self.y
            return EllipticCurvePoint(self.a, self.b, x_3, y_3)
    
    def __mul__(self, scalar: int) -> EllipticCurvePoint:
        """Defines scalar multiplication for EllipticCurvePoint"""
        if isinstance(scalar, int) and scalar >= 0:
            current_term = EllipticCurvePoint(self.a, self.b, self.x, self.y)
            solution = EllipticCurvePoint(self.a, self.b, None, None)
            while scalar:
                if scalar & 1:
                    solution += current_term
                current_term += current_term
                scalar = scalar >> 1
            return solution
        else:
            error = "Incompatible type scalar multiplying with an EllipticCurvePoint"
            raise TypeError(error)
    
    def __rmul__(self, scalar: int) -> EllipticCurvePoint:
        """Defines right scalar multiplication for EllipticCurvePoint"""
        if isinstance(scalar, int) and scalar >= 0:
            current_term = EllipticCurvePoint(self.a, self.b, self.x, self.y)
            solution = EllipticCurvePoint(self.a, self.b, None, None)
            while scalar:
                if scalar & 1:
                    solution += current_term
                current_term += current_term
                scalar = scalar >> 1
            return solution
        else:
            error = "Incompatible type scalar multiplying with an EllipticCurvePoint"
            raise TypeError(error)
    
    def is_same_curve(self, other: EllipticCurvePoint) -> bool:
        """Check if another EllipticCurvePoint is on the same curve as the current one"""
        if isinstance(other, EllipticCurvePoint):
            return ((self.a == other.a) and (self.b == other.b))
        else:
            error = "Incompatible type checking curve parameters with an EllipticCurvePoint"
            raise TypeError(error)
        
    def is_on_curve(self) -> bool:
        """Checks if the given point is on the given elliptic curve"""
        if self.a is not None and self.b is not None:
            return ((self.y**2) == ((self.x**3) + (self.a * self.x) + self.b))
        else:
            error = "One of the parameters (a, b) of the current curve is a None type"
            raise TypeError(error)
