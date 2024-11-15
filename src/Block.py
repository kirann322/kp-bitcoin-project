from __future__ import annotations
from src.utils import (
    bits_to_target,
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    merkle_root
)

class Block:
    def __init__(self, version, prev_block, merkle_root, timestamp, bits, nonce, transaction_hashes = None):
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.transaction_hashes = transaction_hashes

    @classmethod
    def parse_block(cls, byte_stream: bytes) -> Block:
        """Takes a byte stream and parses out a block and returns an instance of a Block object"""
        # version - 4 bytes, little endian, interpret as int
        version = little_endian_to_int(byte_stream.read(4))
        # prev_block - 32 bytes, little endian (use [::-1] to reverse)
        prev_block = byte_stream.read(32)[::-1]
        # merkle_root - 32 bytes, little endian (use [::-1] to reverse)
        merkle_root = byte_stream.read(32)[::-1]
        # timestamp - 4 bytes, little endian, interpret as int
        timestamp = little_endian_to_int(byte_stream.read(4))
        # bits - 4 bytes
        bits = byte_stream.read(4)
        # nonce - 4 bytes
        nonce = byte_stream.read(4)
        return Block(version, prev_block, merkle_root, timestamp, bits, nonce)

    def serialize_block_header(self) -> bytes:
        """Returns the 80 byte block header"""
        # version - 4 bytes, little endian
        result = int_to_little_endian(self.version, 4)
        # prev_block - 32 bytes, little endian
        result += self.prev_block[::-1]
        # merkle_root - 32 bytes, little endian
        result += self.merkle_root[::-1]
        # timestamp - 4 bytes, little endian
        result += int_to_little_endian(self.timestamp, 4)
        # bits - 4 bytes
        result += self.bits
        # nonce - 4 bytes
        result += self.nonce
        return result

    def hash_block(self) -> bytes:
        """Returns the hash256 interpreted little endian of the block"""
        s = self.serialize_block_header()
        sha = hash256(s)
        return sha[::-1]

    def bip9(self) -> bool:
        """Returns whether this block is signaling readiness for BIP9"""
        return self.version >> 29 == 0b001

    def bip91(self) -> bool:
        """Returns whether this block is signaling readiness for BIP91"""
        return self.version >> 4 & 1 == 1

    def bip141(self) -> bool:
        """Returns whether this block is signaling readiness for BIP141"""
        return self.version >> 1 & 1 == 1
    
    def target(self) -> bytes:
        """Returns the proof-of-work target based on the bits"""
        return bits_to_target(self.bits)

    def difficulty(self) -> float:
        """Returns the block difficulty based on the bits using the equation difficulty = (0xffff * 256 ^ (0x1d - 3)) / target"""
        lowest = 0xffff * 256**(0x1d - 3)
        return lowest / self.target()

    def check_pow(self) -> bool:
        """Returns whether this block satisfies proof of work"""
        sha = hash256(self.serialize_block_header())
        proof = little_endian_to_int(sha)
        return proof < self.target()
    
    def validate_merkle_root(self) -> bool:
        """Validates a merkle root for the current block"""
        hashes = [h[::-1] for h in self.tx_hashes]
        root = merkle_root(hashes)
        return root[::-1] == self.merkle_root
