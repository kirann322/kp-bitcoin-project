from __future__ import annotations
from FieldElement import FieldElement
from EllipticCurvePoint import EllipticCurvePoint
from utils import hash160, hash256, encode_base58, encode_base58_checksum

import unittest

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
    
    def sec(self, compressed:bool=True) -> bytearray: # rename to serialize_sec or sec2point
        """Returns the SEC (Standards for Efficient Cryptography) serialized format of the point"""
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')
    
    def sqrt(self):
        """Calculates the square root of a secp256k1 point using the formula w = v^(p+1)//4"""
        return self**((CONSTANT_PRIME + 1) // 4)
    
    def hash160(self, compressed=True):
        """Returns the hash160 for the secp256k1 point"""
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        """Returns the address string"""
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)
    
    @classmethod
    def parse(self, sec_bin): # rename to deserialize_sec or point2sec
        """reads a S256Point object from a SEC serialized binary (not hex)"""
        if sec_bin[0] == 4: # uncompressed sec format
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x=x, y=y)
        else: # compressed sec format
            x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
            # solving for y in the equation y^2 = x^3 + 7
            right_side = x**3 + S256Field(CONSTANT_B)
            left_side = right_side.sqrt()
            if left_side.num % 2 == 0:
                even_beta = left_side
                odd_beta = S256Field(CONSTANT_PRIME - left_side.num)
            else:
                even_beta = S256Field(CONSTANT_PRIME - left_side.num)
                odd_beta = left_side
            if sec_bin[0] == 2: # value is even
                return S256Point(x, even_beta)
            else: # value is odd
                return S256Point(x, odd_beta)

class TestS256Field(unittest.TestCase):
    import PrivateKey
    def test_sec_uncompressed(self):
        tests = [5000, 2018**5, 0xdeadbeef12345]
        solutions = [
            "04ffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c315dc72890a4f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10",
            "04027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9dff87647fd023c13b4a4994f17691895806e1b40b57f4fd22581a4f46851f3b06",
            "04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd59961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121",
        ]
        for idx, test in enumerate(tests):
            pk = PrivateKey.PrivateKey(test)
            self.assertEqual(pk.point.sec(compressed=False), bytearray.fromhex(solutions[idx]))
    
    def test_sec_compressed(self):
        tests = [5001, 2019**5, 0xdeadbeef54321]
        solutions = [
            "0357a4f368868a8a6d572991e484e664810ff14c05c0fa023275251151fe0e53d1",
            "02933ec2d2b111b92737ec12f1c5d20f3233a0ad21cd8b36d0bca7a0cfa5cb8701",
            "0296be5b1292f6c856b3c5654e886fc13511462059089cdf9c479623bfcbe77690",
        ]
        for idx, test in enumerate(tests):
            pk = PrivateKey.PrivateKey(test)
            self.assertEqual(pk.point.sec(compressed=True), bytearray.fromhex(solutions[idx]))
    
    def test_address(self):
        tests = [5002, 2020**5, 0x12345deadbeef]
        solutions = [
            "1BMERxWc9yF8gYAob2FkngUJgnHuB8AUaN",
            "19JYTuj9fg6aeS7apjuDpJoN9g7Y9ztYXT",
            "1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1",
        ]
        for idx, test in enumerate(tests):
            pk = PrivateKey.PrivateKey(test)
            self.assertEqual(pk.point.address(compressed=True), solutions[idx])

if __name__ == '__main__':
    unittest.main()
