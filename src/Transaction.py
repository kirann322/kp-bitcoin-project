from __future__ import annotations
from io import BytesIO
from src.utils import hash256, little_endian_to_int, decode_varint, int_to_little_endian, encode_varint, SIGHASH_ALL
from src.Script import Script

import json
import requests

class Transaction:
    """Transaction class contains the contents of a transaction, which typically consists of the version, input, output, and locktime."""
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self) -> str:
        """Returns string representation of Transaction"""
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return f"tx: {self.id()}\nversion: {self.version}\ntx_ins:\n{tx_ins}tx_outs:\n{tx_outs}locktime: {self.locktime}"

    def id(self) -> bytes:
        """Returns a human-readable hexadecimal form of the transaction hash"""
        return self.hash().hex()

    def hash(self) -> bytes:
        """Returns a binary hash of the byte serialization of the transaction"""
        return hash256(self.serialize_transaction())[::-1]
    
    @classmethod
    def parse_transaction(cls, byte_string: bytes, testnet: bool = False) -> Transaction:
        """Returns a Transaction instance from an input byte stream"""
        version = little_endian_to_int(byte_string.read(4))
        num_inputs = decode_varint(byte_string)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TransactionInput.parse_transaction_input(byte_string))
        num_outputs = decode_varint(byte_string)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TransactionOutput.parse_transaction_output(byte_string))
        locktime = little_endian_to_int(byte_string.read(4))
        return Transaction(version, inputs, outputs, locktime, testnet=testnet)
    
    def serialize_transaction(self) -> bytes:
        """Returns the byte serialization of the transaction"""
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize_transaction_input()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize_transaction_output()
        result += int_to_little_endian(self.locktime, 4)
        return result
    
    def fee(self):
        """Returns the fee of this transaction in satoshi"""
        input_sum, output_sum = 0, 0
        for tx_in in self.tx_ins:
            input_sum += tx_in.value(self.testnet)
        for tx_out in self.tx_outs:
            output_sum += tx_out.amount
        return input_sum - output_sum
    
    def sig_hash(self, input_index):
        s = int_to_little_endian(self.version, 4)
        s += encode_varint(len(self.tx_ins))
        for i, tx_in in enumerate(self.tx_ins):
            if i == input_index:
                s += TransactionInput(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    script_sig=tx_in.script_pubkey(self.testnet),
                    sequence=tx_in.sequence,
                ).serialize_transaction_input()
            else:
                s += TransactionInput(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    sequence=tx_in.sequence,
                ).serialize_transaction_input()
        s += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            s += tx_out.serialize_transaction_output()
        s += int_to_little_endian(self.locktime, 4)
        s += int_to_little_endian(SIGHASH_ALL, 4)
        h256 = hash256(s)
        return int.from_bytes(h256, 'big')
    
    def verify_input(self, input_index):
        tx_in = self.tx_ins[input_index]
        script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
        z = self.sig_hash(input_index)
        combined = [tx_in.script_sig] + [script_pubkey]
        combined = Script(cmds = combined)
        return combined.evaluate(z)
    
    def verify(self):
        """Verifies a transaction"""
        if self.fee() < 0:
            return False
        for i in range(len(self.tx_ins)):
            if not self.verify_input(i):
                return False
        return True
    
    def sign_input(self, input_index, private_key):
        z = self.sig_hash(input_index)
        der = private_key.sign(z).serialize_to_der_bytes()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.serialize_to_sec_bytes()
        self.tx_ins[input_index].script_sig = Script([sig, sec])
        return self.verify_input(input_index)
    
    def is_coinbase(self) -> bool:
        """Returns whether or not the transaction is a coinbase transaction"""
        if len(self.tx_ins) != 1:
            return False
        first_input = self.tx_ins[0]
        if first_input.prev_tx != b'\x00' * 32:
            return False
        if first_input.prev_index != 0xffffffff:
            return False
        return True
    
    def coinbase_height(self) -> int:
        """Returns the height of the transaction by reading it from a coinbase transaction as defined in BIP0034"""
        if not self.is_coinbase():
            return None
        element = self.tx_ins[0].script_sig.cmds[0]
        return little_endian_to_int(element)


class TransactionInput:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    @classmethod
    def parse_transaction_input(cls, byte_stream: bytes) -> TransactionInput:
        """Returns a TransactionInput instance given a byte stream"""
        prev_tx = byte_stream.read(32)[::-1]
        prev_index = little_endian_to_int(byte_stream.read(4))
        script_sig = Script.parse_script(byte_stream)
        sequence = little_endian_to_int(byte_stream.read(4))
        return TransactionInput(prev_tx, prev_index, script_sig, sequence)
    
    def serialize_transaction_input(self) -> bytes:
        """Returns the byte serialization of the transaction input"""
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize_script()
        result += int_to_little_endian(self.sequence, 4)
        return result
    
    def fetch_transaction(self, testnet=False) -> TransactionFetcher:
        """Fetches the transaction from the testnet"""
        return TransactionFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        """Get the output value by looking up the transaction hash and returns the amount in satoshi"""
        tx = self.fetch_transaction(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        """Get the Script Public Key by looking up the tx hash and returns a Script object"""
        tx = self.fetch_transaction(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey


class TransactionOutput:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return f"{self.amount}:{self.script_pubkey}"
    
    @classmethod
    def parse_transaction_output(cls, byte_stream: bytes) -> TransactionOutput:
        """Returns a TransactionOutput instance given a byte stream"""
        amount = little_endian_to_int(byte_stream.read(8))
        script_pubkey = Script.parse_script(byte_stream)
        return cls(amount, script_pubkey)
    
    def serialize_transaction_output(self) -> bytes:
        """Returns the byte serialization of the transaction output"""
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize_script()
        return result


class TransactionFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'https://blockstream.info/testnet/api/'
        else:
            return 'https://blockstream.info/api/'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = f"{cls.get_url(testnet)}/tx/{tx_id}/hex"
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}'.format(response.text))
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Transaction.parse_transaction(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Transaction.parse_transaction(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError(f"not the same id: {tx.id()} vs {tx_id}")
            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]
    
    @classmethod
    def load_cache(cls, filename):
        disk_cache = json.loads(open(filename, 'r').read())
        for k, raw_hex in disk_cache.items():
            raw = bytes.fromhex(raw_hex)
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Transaction.parse_transaction(BytesIO(raw))
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Transaction.parse_transaction(BytesIO(raw))
            cls.cache[k] = tx

    @classmethod
    def dump_cache(cls, filename):
        with open(filename, 'w') as f:
            to_dump = {k: tx.serialize_transaction().hex() for k, tx in cls.cache.items()}
            s = json.dumps(to_dump, sort_keys=True, indent=4)
            f.write(s)
