from Container import *
import sys

TEST_FILE_NAME = 'test.txt'
TEST_CONTAINER_NAME = 'test-container.si'
TEST_BLOCK_SIZE = 32


def testCreate():
    src_file = open(TEST_FILE_NAME, 'rb')
    src_file.seek(0, 2)
    filesize = src_file.tell()
    src_file.seek(0)

    dst_file = open(TEST_CONTAINER_NAME, 'wb')
    hdr = Header(MAGIC_WORD.value, None)
    hdr.payload = RAW
    hdr.header_size = sys.getsizeof(hdr)

    dst_file.write(hdr.castForFile())
    dst_file.write(str.encode('\n'))

    name_length = len(TEST_FILE_NAME)
    md = MetadataFile(None, filesize, TEST_BLOCK_SIZE, int(filesize / (TEST_BLOCK_SIZE / 8)))
    md.length = sys.getsizeof(md) + name_length + 1
    if filesize % (TEST_BLOCK_SIZE / 8) > 0:
        md.block_count += 1
    dst_file.write(md.castForFile())
    dst_file.write(str.encode(TEST_FILE_NAME))

    dst_file.write(str.encode('\n'))
    for block in range(md.block_count):
        src_file.seek(block * int(TEST_BLOCK_SIZE / 8))
        buffer = src_file.read(int(TEST_BLOCK_SIZE / 8)).decode().replace('\r\n', '\n')
        dst_file.write(buffer.encode())
    src_file.close()
    dst_file.close()


def testExtract():
    src_file = open(TEST_CONTAINER_NAME, 'rb')
    buffer_hdr = src_file.readline()
    hdr = Header(int.from_bytes(buffer_hdr[:4], 'little'), int.from_bytes(buffer_hdr[4:8], 'little'),
                 int.from_bytes(buffer_hdr[8:12], 'little'), int.from_bytes(buffer_hdr[12:16], 'little'))
    if hdr.magic_word != MAGIC_WORD.value:
        print('FILE IS WRONG')
        return
    if hdr.payload != RAW:
        print('WRONG DATA IN FILE')
        return
    buffer_md = src_file.readline()
    md = MetadataFile(int.from_bytes(buffer_md[:4], 'little'), int.from_bytes(buffer_md[4:8], 'little'),
                      int.from_bytes(buffer_md[8:12], 'little'), int.from_bytes(buffer_md[12:16], 'little'))
    original_name = buffer_md[16:].decode().split('\n')[0]
    dst_file = open('Extract_' + original_name, 'w')
    while md.orig_length > 0:
        buffer = src_file.read(int(TEST_BLOCK_SIZE / 8))
        bytes_to_write = min(4, md.orig_length)
        dst_file.write(buffer.decode())
        md.orig_length -= bytes_to_write

testCreate()
testExtract()
