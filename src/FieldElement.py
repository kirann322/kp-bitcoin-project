from __future__ import annotations

class FieldElement:
    def __init__(self, prime: int, num: int) -> None:
        if num >= prime or num < 0:
            error = "Num {} not in field range 0 to {}".format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self) -> str:
        return "FieldElement_{}({})".format(self.prime, self.num)
    
    def __eq__(self, other: FieldElement) -> bool:
        if other is None:
            error = "None type value passed as parameter to == operator"
            raise TypeError(error)
        return self.num == other.num and self.prime == other.prime
    
    def __ne__(self, other: FieldElement) -> bool:
        if other is None:
            error = "None type value passed as parameter to != operator"
            raise TypeError(error)
        return self.num != other.num or self.prime != other.prime
    
    def __add__(self, other: FieldElement):
        if other is None:
            error = "None type value passed as parameter to + operator"
            raise TypeError(error)
        if self.prime != other.prime:
            error = "Prime values must be the same across Field Elements when adding, {} is not equal to {}".format(self.prime, other.prime)
            raise ValueError
        return FieldElement(self.prime, (self.num + other.num) % self.prime)
    
    def __sub__(self, other: FieldElement):
        if other is None:
            error = "None type value passed as parameter to - operator"
            raise TypeError(error)
        if self.prime != other.prime:
            error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
            raise ValueError
        return FieldElement(self.prime, (self.num - other.num) % self.prime)
    
    def __mul__(self, other: FieldElement):
        if other is None:
            error = "None type value passed as parameter to * operator"
            raise TypeError(error)
        if self.prime != other.prime:
            error = "Prime values must be the same across Field Elements when multiplying, {} is not equal to {}".format(self.prime, other.prime)
            raise ValueError
        return FieldElement(self.prime, (self.num * other.num) % self.prime)
    
    def __pow__(self, exponent: int):
        if exponent is None:
            error = "None type value passed as parameter to ** operator"
            raise TypeError(error)
        num = pow(self.num, exponent % (self.prime - 1), self.prime)
        return FieldElement(self.prime, num % self.prime)
    
    def __truediv__(self, other: FieldElement):
        if other is None:
            error = "None type value passed as parameter to / operator"
            raise TypeError(error)
        if self.prime != other.prime:
            error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
            raise ValueError
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return FieldElement(self.prime, num)
