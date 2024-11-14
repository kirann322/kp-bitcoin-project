import unittest
import hashlib

CONSTANT_A = 0
CONSTANT_B = 7
CONSTANT_PRIME = (2**256 - 2**32 - 977)
CONSTANT_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
CONSTANT_GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
CONSTANT_GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
CONSTANT_SECONDS_IN_TWO_WEEKS = 60*60*24*14
SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def hash160(input) -> bytes:
    """Runs a sha256 hash followed by a ripemd160 hash on the input"""
    return hashlib.new('ripemd160', hashlib.sha256(input).digest()).digest()

def hash256(input) -> bytes:
    """Runs a sha256 hash followed by another sha256 hash on the input"""
    return hashlib.sha256(hashlib.sha256(input).digest()).digest()

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

def bits_to_target(bits: bytes) -> int:
    """Returns the target value computed from the bits field using the equation target = coefficient * 256 ^ (exponent-3)"""
    exponent = bits[-1]
    coefficient = little_endian_to_int(bits[:-1])
    return coefficient * 256**(exponent - 3)

def target_to_bits(target: int) -> bytes:
    """Turns a target integer back into bits"""
    raw_bytes = target.to_bytes(32, 'big')
    raw_bytes = raw_bytes.lstrip(b'\x00')  
    if raw_bytes[0] > 0x7f:  
        exponent = len(raw_bytes) + 1
        coefficient = b'\x00' + raw_bytes[:2]
    else:
        exponent = len(raw_bytes)  
        coefficient = raw_bytes[:3]  
    new_bits = coefficient[::-1] + bytes([exponent])  
    return new_bits

def calculate_new_bits(previous_bits: bytes, time_differential: int) -> bytes:
    if time_differential > CONSTANT_SECONDS_IN_TWO_WEEKS * 4:
        time_differential = CONSTANT_SECONDS_IN_TWO_WEEKS * 4
    if time_differential < CONSTANT_SECONDS_IN_TWO_WEEKS // 4:
        time_differential = CONSTANT_SECONDS_IN_TWO_WEEKS // 4
    new_target = bits_to_target(previous_bits) * time_differential // CONSTANT_SECONDS_IN_TWO_WEEKS
    return target_to_bits(new_target)

def merkle_parent(hash1, hash2) -> bytes:
    """Takes the binary hashes and calculates the hash256"""
    return hash256(hash1 + hash2)

def merkle_parent_level(hashes):
    """Takes a list of binary hashes and returns a list that's half the length"""
    if len(hashes) == 1:
        raise RuntimeError('Cannot take a parent level with only 1 item')
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    parent_level = []
    for i in range(0, len(hashes), 2):
        parent = merkle_parent(hashes[i], hashes[i + 1])
        parent_level.append(parent)
    return parent_level

def merkle_root(hashes):
    """Takes a list of binary hashes and returns the merkle root"""
    current_level = hashes
    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)
    return current_level[0]

def bytes_to_bit_field(some_bytes):
    flag_bits = []
    for byte in some_bytes:
        for _ in range(8):
            flag_bits.append(byte & 1)
            byte >>= 1
    return flag_bits

def bit_field_to_bytes(bit_field):
    if len(bit_field) % 8 != 0:
        raise RuntimeError('bit_field does not have a length that is divisible by 8')
    result = bytearray(len(bit_field) // 8)
    for i, bit in enumerate(bit_field):
        byte_index, bit_index = divmod(i, 8)
        if bit:
            result[byte_index] |= 1 << bit_index
    return bytes(result)


def bytes_to_bit_field(some_bytes):
    flag_bits = []
    # iterate over each byte of flags
    for byte in some_bytes:
        # iterate over each bit, right-to-left
        for _ in range(8):
            # add the current bit (byte & 1)
            flag_bits.append(byte & 1)
            # rightshift the byte 1
            byte >>= 1
    return flag_bits


def murmur3(data, seed=0):
    '''from http://stackoverflow.com/questions/13305290/is-there-a-pure-python-implementation-of-murmurhash'''
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    length = len(data)
    h1 = seed
    roundedEnd = (length & 0xfffffffc)  # round down to 4 byte block
    for i in range(0, roundedEnd, 4):
        # little endian load order
        k1 = (data[i] & 0xff) | ((data[i + 1] & 0xff) << 8) | \
            ((data[i + 2] & 0xff) << 16) | (data[i + 3] << 24)
        k1 *= c1
        k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)  # ROTL32(k1,15)
        k1 *= c2
        h1 ^= k1
        h1 = (h1 << 13) | ((h1 & 0xffffffff) >> 19)  # ROTL32(h1,13)
        h1 = h1 * 5 + 0xe6546b64
    # tail
    k1 = 0
    val = length & 0x03
    if val == 3:
        k1 = (data[roundedEnd + 2] & 0xff) << 16
    # fallthrough
    if val in [2, 3]:
        k1 |= (data[roundedEnd + 1] & 0xff) << 8
    # fallthrough
    if val in [1, 2, 3]:
        k1 |= data[roundedEnd] & 0xff
        k1 *= c1
        k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)  # ROTL32(k1,15)
        k1 *= c2
        h1 ^= k1
    # finalization
    h1 ^= length
    # fmix(h1)
    h1 ^= ((h1 & 0xffffffff) >> 16)
    h1 *= 0x85ebca6b
    h1 ^= ((h1 & 0xffffffff) >> 13)
    h1 *= 0xc2b2ae35
    h1 ^= ((h1 & 0xffffffff) >> 16)
    return h1 & 0xffffffff

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
