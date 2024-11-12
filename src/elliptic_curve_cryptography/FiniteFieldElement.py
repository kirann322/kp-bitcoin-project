from __future__ import annotations
from sympy import isprime

class FiniteFieldElement:
    def __init__(self, prime: int, num: int) -> None:
        """Initialize a finite field element if its order is prime and its value is in field"""
        if not isprime(prime):
            error = f"FiniteFieldElement cannot be created with the non prime value {prime}"
            raise ValueError(error)
        if num >= prime or num < 0:
            num = num % prime
        self.num = num
        self.prime = prime

    def __repr__(self) -> str:
        """Returns string representation of FiniteFieldElement"""
        return f"FFE_{self.prime}({self.num})"
    
    def __eq__(self, other: FiniteFieldElement) -> bool:
        """Checks equality of FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            return (self.num == other.num and self.prime == other.prime)
        elif isinstance(other, int):
            return (self.num == other)
        elif other is None:
            error = "None type value making equality comparison to a FiniteFieldElement"
            raise TypeError(error)
        else:
            error = "Incompatible type making equality comparison to a FiniteFieldElement"
            raise TypeError(error)
    
    def __ne__(self, other: FiniteFieldElement) -> bool:
        """Checks non equality of FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            return (self.num != other.num or self.prime != other.prime)
        elif isinstance(other, int):
            return (self.num != other)
        elif other is None:
            error = "None type value making not equals comparison to a FiniteFieldElement"
            raise TypeError(error)
        else:
            error = "Incompatible type making not equals comparison to a FiniteFieldElement"
            raise TypeError(error)
    
    def __add__(self, other) -> FiniteFieldElement:
        """Defines addition for FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            if self.prime != other.prime:
                error = "Fields of different Prime values must be the same across Field Elements when adding {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FiniteFieldElement(self.prime, (self.num + other.num) % self.prime)
        elif isinstance(other, int):
            return FiniteFieldElement(self.prime, (self.num + other) % self.prime)
        elif other is None:
            error = "None type adding to FiniteFieldElement"
            raise TypeError(error)
        else:
            error = "Incompatible type adding to a FiniteFieldElement"
            raise TypeError(error)
    
    def __radd__(self, other) -> FiniteFieldElement:
        """Defines right addition for FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            if self.prime != other.prime:
                error = "Fields of different Prime values must be the same across Field Elements when adding {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FiniteFieldElement(self.prime, (self.num + other.num) % self.prime)
        elif isinstance(other, int):
            return FiniteFieldElement(self.prime, (self.num + other) % self.prime)
        elif other is None:
            error = "None type adding to FiniteFieldElement"
            raise TypeError(error)
        else:
            error = "Incompatible type adding to a FiniteFieldElement"
            raise TypeError(error)
    
    
    def __sub__(self, other: FiniteFieldElement) -> FiniteFieldElement:
        """Defines subtraction for FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FiniteFieldElement(self.prime, (self.num - other.num) % self.prime)
        elif isinstance(other, int):
            return FiniteFieldElement(self.prime, (self.num - other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to - operator"
            raise TypeError(error)
        else:
            error = "Incompatible type subtracting with a FiniteFieldElement"
            raise TypeError(error)
    
    def __rsub__(self, other: FiniteFieldElement) -> FiniteFieldElement:
        """Defines right subtraction for FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FiniteFieldElement(self.prime, (self.num - other.num) % self.prime)
        elif isinstance(other, int):
            return FiniteFieldElement(self.prime, (self.num - other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to - operator"
            raise TypeError(error)
        else:
            error = "Incompatible type subtracting with a FiniteFieldElement"
            raise TypeError(error)
    
    def __mul__(self, other: FiniteFieldElement) -> FiniteFieldElement:
        """Defines multiplication for FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when multiplying, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FiniteFieldElement(self.prime, (self.num * other.num) % self.prime)
        elif isinstance(other, int):
            return FiniteFieldElement(self.prime, (self.num * other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to * operator"
            raise TypeError(error)
        else:
            error = "Incompatible type multiplying with a FiniteFieldElement"
            raise TypeError(error)
    
    def __rmul__(self, other: FiniteFieldElement) -> FiniteFieldElement:
        """Defines right multiplication for FiniteFieldElement with other objects"""
        if isinstance(other, FiniteFieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when multiplying, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            return FiniteFieldElement(self.prime, (self.num * other.num) % self.prime)
        elif isinstance(other, int):
            return FiniteFieldElement(self.prime, (self.num * other) % self.prime)
        elif other is None:
            error = "None type value passed as parameter to * operator"
            raise TypeError(error)
        else:
            error = "Incompatible type multiplying with a FiniteFieldElement"
            raise TypeError(error)
        
    
    def __pow__(self, exponent: int) -> FiniteFieldElement:
        """Defines exponentiation for FiniteFieldElement"""
        if exponent is None:
            error = "None type value passed as parameter to ** operator"
            raise TypeError(error)
        num = pow(self.num, exponent % (self.prime - 1), self.prime)
        return FiniteFieldElement(self.prime, num % self.prime)
    
    def __truediv__(self, other: FiniteFieldElement) -> FiniteFieldElement:
        """Defines regular division for FiniteFieldElement using the equation a / b = a * (b**(prime-2)) % prime"""
        if isinstance(other, FiniteFieldElement):
            if self.prime != other.prime:
                error = "Prime values must be the same across Field Elements when subtracting, {} is not equal to {}".format(self.prime, other.prime)
                raise ValueError
            num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
            return FiniteFieldElement(self.prime, num)
        elif isinstance(other, int):
            num = self.num * pow(other, self.prime - 2, self.prime) % self.prime
            return FiniteFieldElement(self.prime, num)
        elif other is None:
            error = "None type value passed as parameter to / operator"
            raise TypeError(error)
        else:
            error = "Incompatible type dividing with a FiniteFieldElement"
            raise TypeError(error)
