import zlib
from hf import hash_function as hash_funktion
import timeit


def getFiles():
   tusen_byte=''
   tio_tusen_byte=''
   hundra_kb = ''
   en_mb=''

   with open('1000byte.txt', "r", encoding="utf-8") as file:
       for row in file:
           tusen_byte=tusen_byte+row

   with open('10_000byte.txt', "r", encoding="utf-8") as file:
       for row in file:
           tio_tusen_byte=tusen_byte+row


   with open('100_000byte.txt', "r", encoding="utf-8") as file:
       for row in file:
           hundra_kb = hundra_kb + row

   with open('1_000_000byte.txt', "r", encoding="utf-8") as file:
       for row in file:
           en_mb = en_mb + row


   return tusen_byte, tio_tusen_byte, hundra_kb, en_mb



# Tidtagning


def time_adler(en_kb, tio_kb, hundra_kb, en_mb):
# Adler32 klockas

   print("Adler32 med 1 kb tog",timeit.timeit(stmt=lambda: zlib.adler32(en_kb.encode()), number=1) , "sekunder")
   print("Adler32 med 10 kb tog", timeit.timeit(stmt=lambda: zlib.adler32(tio_kb.encode()), number=1), "sekunder")
   print("Adler32 med 100 kb tog", timeit.timeit(stmt=lambda: zlib.adler32(hundra_kb.encode()), number=1), "sekunder")
   print("Adler32 med 1 Mb tog", timeit.timeit(stmt=lambda: zlib.adler32(en_mb.encode()), number=1), "sekunder")


def time_hash(en_kb, tio_kb, hundra_kb, en_mb):
# Den egna hashfunktionen klockas

   print("Hashen med 1 kb tog",timeit.timeit(stmt=lambda: hash_funktion(en_kb), number=1) , "sekunder")
   print("Hashen med 10 kb tog", timeit.timeit(stmt=lambda:  hash_funktion(tio_kb), number=1), "sekunder")
   print("Hashen med 100 kb tog", timeit.timeit(stmt=lambda:  hash_funktion(hundra_kb), number=1), "sekunder")
   print("Hashen med 1 Mb tog", timeit.timeit(stmt=lambda:  hash_funktion(en_mb), number=1), "sekunder")


def time():
   # The test is started

   en_kb, tio_kb, hundra_kb, en_mb = getFiles()
   time_adler(en_kb, tio_kb, hundra_kb, en_mb)
   time_hash(en_kb, tio_kb, hundra_kb, en_mb)

if __name__ == '__main__':
   time()
