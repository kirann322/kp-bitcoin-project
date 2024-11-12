from random import randint
from src.elliptic_curve_cryptography.FiniteFieldElement import *
from src.elliptic_curve_cryptography.Secp256k1Curve import *
from src.elliptic_curve_cryptography.DigitalSignature import *

import unittest

class TestSignature(unittest.TestCase):
    def test_serialize_to_der_bytes(self):
        tests = [(0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec)]
        solutions = [
            "3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec",
        ]
        for idx, test in enumerate(tests):
            sig = Signature(test[0], test[1])
            self.assertEqual(sig.serialize_to_der_bytes(), bytearray.fromhex(solutions[idx]))
        testcases = (
            (1, 2),
            (randint(0, 2**256), randint(0, 2**255)),
            (randint(0, 2**256), randint(0, 2**255)),
        )
        for r, s in testcases:
            sig = Signature(r, s)
            der = sig.serialize_to_der_bytes()
            sig2 = Signature.parse_signature(der)
            self.assertEqual(sig2.r, r)
            self.assertEqual(sig2.s, s)

class PrivateKeyTest(unittest.TestCase):
    def test_sign(self):
        pk = PrivateKey(randint(0, CONSTANT_N))
        z = randint(0, 2**256)
        sig = pk.sign(z)
        self.assertTrue(pk.point.verify(z, sig))

    def test_wif(self):
        pk = PrivateKey(2**256 - 2**199)
        expected = 'L5oLkpV3aqBJ4BgssVAsax1iRa77G5CVYnv9adQ6Z87te7TyUdSC'
        self.assertEqual(pk.wif(compressed=True, testnet=False), expected)
        pk = PrivateKey(2**256 - 2**201)
        expected = '93XfLeifX7Jx7n7ELGMAf1SUR6f9kgQs8Xke8WStMwUtrDucMzn'
        self.assertEqual(pk.wif(compressed=False, testnet=True), expected)
        pk = PrivateKey(0x0dba685b4511dbd3d368e5c4358a1277de9486447af7b3604a69b8d9d8b7889d)
        expected = '5HvLFPDVgFZRK9cd4C5jcWki5Skz6fmKqi1GQJf5ZoMofid2Dty'
        self.assertEqual(pk.wif(compressed=False, testnet=False), expected)
        pk = PrivateKey(0x1cca23de92fd1862fb5b76e5f4f50eb082165e5191e116c18ed1a6b24be6a53f)
        expected = 'cNYfWuhDpbNM1JWc3c6JTrtrFVxU4AGhUKgw5f93NP2QaBqmxKkg'
        self.assertEqual(pk.wif(compressed=True, testnet=True), expected)

if __name__ == '__main__':
    unittest.main()
