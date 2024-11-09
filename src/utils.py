import unittest
import hashlib

CONSTANT_A = 0
CONSTANT_B = 7
CONSTANT_PRIME = (2**256 - 2**32 - 977)
CONSTANT_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
CONSTANT_GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
CONSTANT_GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def hash160(s):
    '''sha256 followed by ripemd160'''
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def hash256(s):
    '''two rounds of sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def encode_base58(byte_string: bytes) -> str:
    """Encodes an array of bytes into a base58 encoded string"""
    BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    index = 0
    while byte_string[index] == 0:
        index += 1
    num = int.from_bytes(byte_string, 'big')
    prefix = '1' * index
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum, hash256(combined[:-4])[:4]))
    return combined[1:-4]


def little_endian_to_int(b: bytes) -> int:
    """little_endian_to_int takes byte sequence as a little-endian number, returns an integer"""
    return int.from_bytes(b, 'little')


def int_to_little_endian(n: int, length: int) -> bytes:
    """endian_to_little_endian takes an integer and returns the little-endian byte sequence of length"""
    return n.to_bytes(length, 'little')

def decode_varint(byte_string: bytes) -> int:
    """Decodes a byte stream into a variable integer"""
    i = byte_string.read(1)[0]
    if i < 0xfd:
        return i
    if i == 0xfd:
        return little_endian_to_int(byte_string.read(2))
    elif i == 0xfe:
        return little_endian_to_int(byte_string.read(4))
    elif i == 0xff:
        return little_endian_to_int(byte_string.read(8))
    else:
        raise ValueError(f"byte value {byte_string} cannot be decoded as varint")

def encode_varint(num: int) -> bytes:
    """Encodes an integer as a varint"""
    if num < 0xfd:
        return bytes([num])
    elif num < 0x10000:
        return b'\xfd' + int_to_little_endian(num, 2)
    elif num < 0x100000000:
        return b'\xfe' + int_to_little_endian(num, 4)
    elif num < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(num, 8)
    else:
        raise ValueError(f"integer {num} too large to encode as varint")

class TestUtils(unittest.TestCase):
    def test_encode_base58(self):
        tests = [
            "7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d",
            "eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c",
            "c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6",
        ]
        solutions = [
            "9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6",
            "4fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd",
            "EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7",
        ]
        for idx, test in enumerate(tests):
            self.assertEqual(encode_base58(bytes.fromhex(test)), solutions[idx])

if __name__ == '__main__':
    unittest.main()
