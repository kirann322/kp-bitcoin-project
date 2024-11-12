from __future__ import annotations
from src.elliptic_curve_cryptography.FiniteFieldElement import FiniteFieldElement
from src.elliptic_curve_cryptography.EllipticCurvePoint import EllipticCurvePoint
from src.utils import hash160, encode_base58_checksum

CONSTANT_A = 0
CONSTANT_B = 7
CONSTANT_SECP256K1_PRIME = (2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1)
CONSTANT_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
CONSTANT_GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
CONSTANT_GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
"""
CONSTANT_G = EllipticCurvePoint(
        a = FiniteFieldElement(prime=CONSTANT_SECP256K1_PRIME, num=CONSTANT_A),
        b = FiniteFieldElement(prime=CONSTANT_SECP256K1_PRIME, num=CONSTANT_B),
        x = FiniteFieldElement(prime=CONSTANT_SECP256K1_PRIME, num=CONSTANT_GX),
        y = FiniteFieldElement(prime=CONSTANT_SECP256K1_PRIME, num=CONSTANT_GY)
    )
"""

class Secp256k1Element(FiniteFieldElement):
    def __init__(self, num: int):
        """Initialize a finite field element of order CONSTANT_SECP256K1_PRIME"""
        super().__init__(prime = CONSTANT_SECP256K1_PRIME, num = num)

    def __repr__(self) -> str:
        """Returns string representation of Secp256k1Element"""
        return f"{hex(self.num)}".zfill(64)
    
    def sqrt(self) -> Secp256k1Element:
        """Calculates the square root of a secp256k1 element using the formula w = v^(p+1)//4"""
        return self**((CONSTANT_SECP256K1_PRIME + 1) // 4)

class Secp256k1Point(EllipticCurvePoint):
    def __init__(self, x, y):
        """Initialize a elliptic curve point along the seckp256k1 curve"""
        a, b = Secp256k1Element(CONSTANT_A), Secp256k1Element(CONSTANT_B)
        if isinstance(x, int):
            x = Secp256k1Element(x)
        if isinstance(y, int):
            y = Secp256k1Element(y)
        super().__init__(x=x, y=y, a=a, b=b)
    
    def __repr__(self) -> str:
        """Returns string representation of Secp256k1Point"""
        if self.x is None:
            return "Secp256k1Point(infinity)"
        else:
            return f"Secp256k1Point({hex(self.x.num)}, {hex(self.y.num)})"
        
    def __rmul__(self, coefficient: int) -> Secp256k1Point:
        """Defines scalar multiplication for Secp256k1Point"""
        coef = coefficient % CONSTANT_N
        result = super().__rmul__(coef)
        return Secp256k1Point(result.x, result.y)
    
    def verify(self, z, signature) -> bool:
        """Returns whether a signature is verifiable"""
        s_inv = pow(signature.s, CONSTANT_N - 2, CONSTANT_N)
        u = z * s_inv % CONSTANT_N 
        v = signature.r * s_inv % CONSTANT_N
        total = u * Secp256k1Point(CONSTANT_GX, CONSTANT_GY) + v * self
        return (total.x.num == signature.r)
    
    def serialize_to_sec_bytes(self, compressed: bool = True) -> bytearray:
        """Returns the SEC (Standards for Efficient Cryptography) serialized format of the point in bytes"""
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')
    
    def hash160(self, compressed: bool = True) -> bytes:
        """Returns the hash160 for the serialized point"""
        return hash160(self.serialize_to_sec_bytes(compressed))

    def address(self, compressed: bool = True, testnet: bool = False) -> str:
        """Returns the address string"""
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)
    
    @classmethod
    def parse_secp256k1_point(self, byte_stream: bytes) -> Secp256k1Point:
        """reads a S256Point object from a SEC serialized binary (not hex)"""
        if byte_stream[0] == 4: # uncompressed sec format
            x = int.from_bytes(byte_stream[1:33], 'big')
            y = int.from_bytes(byte_stream[33:65], 'big')
            return Secp256k1Point(x=x, y=y)
        else: # compressed sec format
            x = Secp256k1Element(int.from_bytes(byte_stream[1:], 'big'))
            # solving for y in the equation y^2 = x^3 + 7
            right_side = x**3 + Secp256k1Element(CONSTANT_B)
            left_side = right_side.sqrt()
            if left_side.num % 2 == 0:
                even_beta = left_side
                odd_beta = Secp256k1Element(CONSTANT_SECP256K1_PRIME - left_side.num)
            else:
                even_beta = Secp256k1Element(CONSTANT_SECP256K1_PRIME - left_side.num)
                odd_beta = left_side
            if byte_stream[0] == 2: # value is even
                return Secp256k1Point(x, even_beta)
            else: # value is odd
                return Secp256k1Point(x, odd_beta)
