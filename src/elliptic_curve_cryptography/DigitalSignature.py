from __future__ import annotations
from io import BytesIO
from src.utils import encode_base58_checksum
from src.elliptic_curve_cryptography.Secp256k1Curve import *

import hmac
import hashlib

class Signature:
    def __init__(self, r: int, s: int):
        """Initialize a Signature object"""
        self.r = r
        self.s = s

    def __repr__(self) -> str:
        """Returns string representation of Signature"""
        return f"Signature({self.r}, {self.s})"

    def serialize_to_der_bytes(self) -> bytes:
        """Returns the DER (Distinguished Encoding Rules) encoded signature of the point"""
        r_binary = self.r.to_bytes(32, byteorder='big')
        # remove all null bytes at the beginning
        r_binary = r_binary.lstrip(b'\x00')
        # if rbin has a high bit, add a \x00
        if r_binary[0] & 0x80:
            r_binary = b'\x00' + r_binary
        result = bytes([2, len(r_binary)]) + r_binary
        s_binary = self.s.to_bytes(32, byteorder='big')
        # remove all null bytes at the beginning
        s_binary = s_binary.lstrip(b'\x00')
        # if sbin has a high bit, add a \x00
        if s_binary[0] & 0x80:
            s_binary = b'\x00' + s_binary
        result += bytes([2, len(s_binary)]) + s_binary
        return bytes([0x30, len(result)]) + result

    @classmethod
    def parse_signature(self, signature_binary: bytes) -> Signature:
        """reads a Signature object from a DER serialized binary (not hex)"""
        signature = BytesIO(signature_binary)
        compound = signature.read(1)[0]
        if compound != 0x30:
            raise SyntaxError("Bad Signature")
        length = signature.read(1)[0]
        if length + 2 != len(signature_binary):
            raise SyntaxError("Bad Signature Length")
        marker = signature.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        rlength = signature.read(1)[0]
        r = int.from_bytes(signature.read(rlength), 'big')
        marker = signature.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        slength = signature.read(1)[0]
        s = int.from_bytes(signature.read(slength), 'big')
        if len(signature_binary) != 6 + rlength + slength:
            raise SyntaxError("Signature too long")
        return Signature(r, s)

class PrivateKey:
    def __init__(self, secret):
        """Initialize a PrivateKey object"""
        self.secret = secret
        self.point = secret * CONSTANT_G

    def hex(self) -> str:
        "Returns a string of hex digits for the PrivateKey"
        return "{:x}".format(self.secret).zfill(64)

    def sign(self, z) -> Signature:
        """Returns a Signature object for the given z"""
        k = self.deterministic_k(z)
        r = (k * CONSTANT_G).x.num
        k_inv = pow(k, CONSTANT_N - 2, CONSTANT_N)
        s = (z + r * self.secret) * k_inv % CONSTANT_N
        if s > CONSTANT_N / 2:
            s = CONSTANT_N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        """Creates a deterministic k for the key"""
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > CONSTANT_N:
            z -= CONSTANT_N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if candidate >= 1 and candidate < CONSTANT_N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()
    
    def wif(self, compressed: bool = True, testnet: bool = False) -> bytes:
        """Encodes the secret key in Wallet Import Format (WIF)"""
        secret_bytes = self.secret.to_bytes(32, 'big')
        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)
