import ctypes
import struct

# MAGIC WORD: P*AA
MAGIC_WORD = ctypes.c_uint32(0x0000001 * ord('P') + 0x00000100 * ord('*') + 0x01010000 * ord('A'));
RAW = 0
KEY_DATA = None
PRIVATE_KEY = None
PUBLIC_KEY = None
ENCRYPTED_DATA = None
DH_PARAMS = None
HEADER_SIZE = 12


class Header:
    def __init__(self, magic_word, header_size=None,
                 payload=None, padding=0):
        self.magic_word = magic_word
        self.header_size = header_size
        self.payload = payload
        self.padding = padding

    def castForFile(self):
        return struct.pack('<4I', self.magic_word, self.header_size, self.payload, self.padding)


class MetadataFile:
    def __init__(self, length, orig_length, block_size, block_count):
        self.orig_length = orig_length
        self.block_size = block_size
        self.block_count = block_count
        self.length = length

    def castForFile(self):
        return struct.pack('<4i', self.length, self.orig_length, self.block_size, self.block_count)


class MetadataKey:
    def __init__(self, length, block_count, block_size):
        self.block_size = block_size
        self.block_count = block_count
        self.length = length
