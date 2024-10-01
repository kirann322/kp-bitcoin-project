from __future__ import annotations
from FieldElement import FieldElement
from EllipticCurvePoint import EllipticCurvePoint

CONSTANT_A = 0
CONSTANT_B = 7
CONSTANT_PRIME = (2**256 - 2**32 - 977)
CONSTANT_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
CONSTANT_GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
CONSTANT_GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

class S256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num = num, prime = CONSTANT_PRIME)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

class S256Point(EllipticCurvePoint):
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(CONSTANT_A), S256Field(CONSTANT_B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)
    
    def __repr__(self):
        if self.x is None:
            return "S256Point(infinity)"
        else:
            return f"S256Point({hex(self.x.num)}, {hex(self.y.num)})"
        
    def __rmul__(self, coefficient):
        coef = coefficient % CONSTANT_N
        result = super().__rmul__(coef)
        return S256Point(result.x, result.y, result.a, result.b)
    
    def verify(self, z, signature):
        s_inv = pow(signature.s, CONSTANT_N - 2, CONSTANT_N)
        u = z * s_inv % CONSTANT_N 
        v = signature.r * s_inv % CONSTANT_N
        total = u * S256Point(CONSTANT_GX, CONSTANT_GY) + v * self
        return total.x.num == signature.r

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s
    
    def __repr__(self) -> str:
        return f"Signature({self.r}, {self.s})"
