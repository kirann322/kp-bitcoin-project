import unittest

import src.FieldElement
import src.S256Field
import src.PrivateKey
import src.utils

class TestS256Field(unittest.TestCase):
    def test_sec(self):
        tests = [5000, 2018**5, 0xdeadbeef12345]
        solutions = [
            0x04ffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c315dc72890a4f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10,
            0x04027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9dff87647fd023c13b4a4994f17691895806e1b40b57f4fd22581a4f46851f3b06,
            0x04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd59961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121
        ]
        for idx, test in enumerate(tests):
            pk = PrivateKey(test)
            self.assertEqual(pk.point.sec(compressed=False), solutions[idx].hex())

if __name__ == '__main__':
    unittest.main()
