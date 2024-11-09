from __future__ import annotations
from io import BytesIO
import unittest

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x},{:x})'.format(self.r, self.s)

    def der(self) -> bytes: # rename signature2der
        """
        Returns the DER (Distinguished Encoding Rules) encoded signature of the point.
        """
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
    def parse(self, signature_binary: bytes) -> Signature: # rename der2signature
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

class TestSignature(unittest.TestCase):
    def test_der(self):
        tests = [(0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec)]
        solutions = [
            "3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec",
        ]
        for idx, test in enumerate(tests):
            sig = Signature(test[0], test[1])
            self.assertEqual(sig.der(), bytearray.fromhex(solutions[idx]))

if __name__ == '__main__':
    unittest.main()
