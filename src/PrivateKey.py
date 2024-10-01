from __future__ import annotations
from random import randint
from unittest import TestCase
from S256Field import S256Field, S256Point, Signature

import hmac
import hashlib

CONSTANT_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
CONSTANT_GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
CONSTANT_GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
CONSTANT_G = S256Point(CONSTANT_GX, CONSTANT_GY)

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * CONSTANT_G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = self.deterministic_k(z)
        r = (k * CONSTANT_G).x.num
        k_inv = pow(k, CONSTANT_N - 2, CONSTANT_N)
        s = (z + r * self.secret) * k_inv % CONSTANT_N
        if s > CONSTANT_N / 2:
            s = CONSTANT_N - s
        return Signature(r, s)

    def deterministic_k(self, z):
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

class PrivateKeyTest(TestCase):

    def test_sign(self):
        pk = PrivateKey(randint(0, CONSTANT_N))
        z = randint(0, 2**256)
        sig = pk.sign(z)
        self.assertTrue(pk.point.verify(z, sig))
