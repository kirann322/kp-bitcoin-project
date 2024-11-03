from __future__ import annotations
from sympy import isprime
from utils import CONSTANT_PRIME

class FieldElement:
    def __init__(self, prime: int, num: int) -> None:
        if num >= prime or num < 0:
            error = f"Num {num} not in field range 0 to {prime-1}"
            raise ValueError(error)
        
        if prime == CONSTANT_PRIME or isprime(prime):
            self.num = num
            self.prime = prime
        else:
            error = f"FieldElement cannot be created with non prime value {prime}"
            raise ValueError(error)

    def __repr__(self) -> str:
        return f"F_{self.prime}({self.num})"
    
    def __eq__(self, other: FieldElement) -> bool:
        if isinstance(other, FieldElement):
            return self.num == other.num and self.prime == other.prime
        elif isinstance(other, int):
            return self.num == other
        elif other is None:
            error = "None type value passed as parameter to == operator"
            raise TypeError(error)
        else:
            error = "Incompatible type comparing == to a FieldElement"
            raise TypeError(error)
    
    def __ne__(self, other: FieldElement) -> bool:
        if other is None:
            error = "None type value passed as parameter to != operator"
            raise TypeError(error)
        return self.num != other.num or self.prime != other.prime
    
    def __add__(self, other):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                error = "Fields of different Prime values must be the same across Field Elements when adding {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FieldElement(self.prime, (self.num + other.num) % self.prime)
        elif isinstance(other, int):
            return FieldElement(self.prime, (self.num + other) % self.prime)
        elif other is None:
            error = "None type adding to FieldElement"
            raise TypeError(error)
        else:
            error = "Incompatible type adding to a FieldElement"
            raise TypeError(error)
    
    def __radd__(self, other):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                error = "Fields of different Prime values must be the same across Field Elements when adding {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FieldElement(self.prime, (self.num + other.num) % self.prime)
        elif isinstance(other, int):
            return FieldElement(self.prime, (self.num + other) % self.prime)
        elif other is None:
            error = "None type adding to FieldElement"
            raise TypeError(error)
        else:
            error = "Incompatible type adding to a FieldElement"
            raise TypeError(error)
    
    
    def __sub__(self, other: FieldElement):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FieldElement(self.prime, (self.num - other.num) % self.prime)
        elif isinstance(other, int):
            return FieldElement(self.prime, (self.num - other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to - operator"
            raise TypeError(error)
        else:
            error = "Incompatible type subtracting with a FieldElement"
            raise TypeError(error)
    
    def __rsub__(self, other: FieldElement):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FieldElement(self.prime, (self.num - other.num) % self.prime)
        elif isinstance(other, int):
            return FieldElement(self.prime, (self.num - other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to - operator"
            raise TypeError(error)
        else:
            error = "Incompatible type subtracting with a FieldElement"
            raise TypeError(error)
    
    def __mul__(self, other: FieldElement):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when multiplying, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FieldElement(self.prime, (self.num * other.num) % self.prime)
        elif isinstance(other, int):
            return FieldElement(self.prime, (self.num * other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to * operator"
            raise TypeError(error)
        else:
            error = "Incompatible type multiplying with a FieldElement"
            raise TypeError(error)
    
    def __rmul__(self, other: FieldElement):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when multiplying, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FieldElement(self.prime, (self.num * other.num) % self.prime)
        elif isinstance(other, int):
            return FieldElement(self.prime, (self.num * other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to * operator"
            raise TypeError(error)
        else:
            error = "Incompatible type multiplying with a FieldElement"
            raise TypeError(error)
        
    
    def __pow__(self, exponent: int):
        if exponent is None:
            error = "None type value passed as parameter to ** operator"
            raise TypeError(error)
        num = pow(self.num, exponent % (self.prime - 1), self.prime)
        return FieldElement(self.prime, num % self.prime)
    
    def __truediv__(self, other: FieldElement):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
            return FieldElement(self.prime, num)
        elif isinstance(other, int):
            num = self.num * pow(other, self.prime - 2, self.prime) % self.prime
            return FieldElement(self.prime, num)
        elif other is None:
            error = "None type value passed as parameter to / operator"
            raise TypeError(error)
        else:
            error = "Incompatible type dividing with a FieldElement"
            raise TypeError(error)
