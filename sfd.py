from time import time
from zlib import adler32, crc32

c = 'test'
start = time()
b=(str(c) + 'A' * 10000000).encode()
for i in range(2): c = adler32(b)
print ('Adler32 benchmark: %3f' % (time() - start), 'seconds')

start = time()
for i in range(256*256*256): c = crc32(str(c) + 'A' * 1000)
print ('CRC32 benchmark: %3.1f' % (time() - start), 'seconds')

