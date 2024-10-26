from __future__ import annotations
from FieldElement import FieldElement
from EllipticCurvePoint import EllipticCurvePoint
from utils import hash160, hash256, encode_base58, encode_base58_checksum

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
    
    def sec(self, compressed=True):
        '''returns the binary version of the SEC format'''
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')
    
    def sqrt(self):
        return self**((CONSTANT_PRIME + 1) // 4)
    
    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        '''Returns the address string'''
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)
    
    @classmethod
    def parse(self, sec_bin):
        '''returns a Point object from a SEC binary (not hex)'''
        if sec_bin[0] == 4:  # <1>
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x=x, y=y)
        is_even = sec_bin[0] == 2  # <2>
        x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
        # right side of the equation y^2 = x^3 + 7
        alpha = x**3 + S256Field(CONSTANT_B)
        # solve for left side
        beta = alpha.sqrt()  # <3>
        if beta.num % 2 == 0:  # <4>
            even_beta = beta
            odd_beta = S256Field(CONSTANT_PRIME - beta.num)
        else:
            even_beta = S256Field(CONSTANT_PRIME - beta.num)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s
    
    def __repr__(self) -> str:
        return f"Signature({self.r}, {self.s})"
    
    def der(self):
        rbin = self.r.to_bytes(32, byteorder='big')
        # remove all null bytes at the beginning
        rbin = rbin.lstrip(b'\x00')
        # if rbin has a high bit, add a \x00
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin  # <1>
        sbin = self.s.to_bytes(32, byteorder='big')
        # remove all null bytes at the beginning
        sbin = sbin.lstrip(b'\x00')
        # if sbin has a high bit, add a \x00
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result
    