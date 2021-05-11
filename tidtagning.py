
import timeit
import zlib
import hashlib

import random


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

def hash_funktion(input):
    # Inputen måste vara en sträng
    hash_value = 0
    for i in range(len(input)):
        hash_value = hash_value + i + ord(input[i]) * 2 ** (i)

    return hash_value % (2**32-1)

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

#Kollision

def collison(length):

    # 1 000 000 random strings with the given parameter length are hashed. Each string is either put in the
    # dictionary or registred as a collision. Note the commented row where adler32 is used instead

    used_values={}
    collison_counter=0
    for i in range(1000000):
        temp_str=generatestring(length)
        temp_hash=hash_funktion(temp_str)
        #temp_hash=zlib.adler32(temp_str.encode())
        if temp_hash in used_values and temp_str!=used_values[temp_hash]:
            collison_counter+=1
        else:
            used_values[temp_hash]=temp_str
    return collison_counter


def generatestring(length):
 # A randomly created string with characters from chars is returned
    chars = '1234567890qwertyuiopasdfghjklzxmcnvbQWERTYUIOPASDFGHJKLZXCVBNM'
    string=''
    for i in range(length):
        string=string+chars[(random.randint(0,len(chars)-1))]
    return string





def split(string):
# Turns a string into a list
    return [char for char in string]








def avalanchetest(test_len, test_range):


    counter = 0
    for j in range(test_range):
        # An orignal string with specified length (test_len) is created and hashed.
        # Both are converted to binary to binary numbers. A list is created,
        # which consists of all the characters (in binary form) of the string.

        org_string=generatestring(test_len)
        original_hash=hash_funktion(org_string)
        # original_hash = zlib.adler32(org_string.encode())
        org_string_bit = ''.join(format(ord(i), '08b') for i in org_string)
        old_hash_bit=('{:032b}'.format(original_hash))
        temp_counter = 0
        div=0
        binary_list = [org_string_bit[i:i + 8] for i in range(0, len(org_string_bit), 8)]

        # If the string is long every tenth character in the string will get a bit replaced.
        # If the new binary number is consists of the characters we want to perform
        # test with, the Hammin-distance is added to a counter. Lastly we get the avarage
        # distance for all new strings

        if test_len>999:

            for j in range(len(binary_list)//10):
                for i in range(0, 8):
                    new_binary = replace_bit(binary_list[10*j], i, binary_list, 10*j)
                    if new_binary:
                        temp_counter += get_dif(new_binary, old_hash_bit)
                        div += 1
            counter += temp_counter / (div)

        # The same as above, but with a new intervall (all characters are replaced.

        else:

            for j in range(len(binary_list)):
                for i in  range(0,8):
                    new_binary=replace_bit(binary_list[j],i, binary_list, j)
                    if new_binary:
                        temp_counter += get_dif(new_binary, old_hash_bit)
                        div += 1
            counter += temp_counter / (div)


    print('Ändrade bitar: ', counter / test_range, ' Ändring/32bit', counter / (32 * test_range))


def get_dif(new_binary, old_hash_bit):
    # We create a string fro ma binary number, which is later hashed and
    # converted to a binary number. We then return the hammin-distance
    # between se hash values.

    new_string = "".join([chr(int(new_binary[i:i + 8], 2)) for i in range(0, len(new_binary), 8)])
    new_hash = hash_funktion(new_string)
    # new_hash = zlib.adler32(new_string.encode())
    new_hash_bit = ('{:032b}'.format(new_hash))
    return get_hammin(old_hash_bit, new_hash_bit)

def get_hammin(old_hash, new_hash):
    #The Hammin-distance between 2 binary numbers is returned.
    count=0
    for i in range(len(old_hash)):
        if old_hash[i]!=new_hash[i]:
            count+=1
    return count

def replace_bit(binary_char, index_in_char, binary_string_list, index_in_string):
    # We replace a bit in a character in a specified index. If the new character is one
    # of characters we want to test, we return a copy of the original binary string (divided into a list),
    # but with the newly created character.
    temp_list = [char for char in binary_char]
    if temp_list[index_in_char] == '0':
        temp_list[index_in_char] = '1'
    else:
        temp_list[index_in_char] = '0'
    bin_data = ''.join(temp_list)

    if int(bin_data,2)<32 or int(bin_data,2)>127:
        return False
    copied_string=list(binary_string_list)
    copied_string[index_in_string]=bin_data
    return ''.join(copied_string)


def hashfunktion(namn):
   summa = 0
   for tkn in namn:
      summa = summa*365 + ord(tkn)
   return summa % 7 + 1



def collision_test ():
# the test is started
print ( collison ( 20 ))
print ( collison ( 25 ))
print ( collison ( 30 ))
print ( collison ( 35 ))
print ( collison ( 40 ))
print ( collison ( 45 ))
print ( collison ( 50 ))
def collison ( length ):
    # 1 000 000 random strings with the given parameter length are hashed . Each string is either put in the
    # dictionary or registered as a collision . Note the commented row where adler32 is used instead
    used_values ={}
collison_counter =0
for i in range ( 1000000 ):
temp_str = generatestring ( length )
temp_hash = hash_funktion ( temp_str )
# temp_hash = zlib . adler32 ( temp_str . encode ())
if temp_hash in used_values and temp_str != used_values [ temp_hash ]:
collison_counter +=1
else :
used_values [ temp_hash ]= temp_str
return collison_counter
def generatestring ( length ):
# A randomly created string with characters from chars is returned
chars = ’ 1234567890qwertyuiopasdfghjklzxmcnvbQWERTYUIOPASDFGHJKLZXCVBNM ’
string =’’
for i in range ( length ):
string = string + chars [( random . randint (0 , len ( chars )-1))]
return string




def avalanchetest_hash(test_len, test_range, long):
    chars = '1234567890qwertyuiopasdfghjklzxmcnvbQWERTYUIOPASDFGHJKLZXCVBNM'
    counter = 0
    variotions = None

    for j in range(test_range):

        org_string = generatestring(test_len)
        original_hash = hash_funktion(org_string)
        org_string_bit = ''.join(format(ord(i), '08b') for i in org_string)
        old_hash_bit = (get_bin32(hash_funktion(org_string)))
        temp_counter = 0
        div=0
        if long:
            variotions = 1000
        else:
            variotions = len(org_string_bit)

        for i in range(variotions):
            if i%8!=0:
                new_string = change_bit(org_string_bit, i)
                # print(''.join(format(ord(i), '08b') for i in new_string))
                h=hash_funktion(new_string)
                new_hash_bit = (get_bin32(hash_funktion(new_string)))
                dif = (compare_hash(old_hash_bit, new_hash_bit))
                temp_counter += dif
                div+=1
        counter += temp_counter / (div)
    print('Ändrade bitar: ', counter / test_range, ' Ändring/32bit', counter / (32 * test_range))


def avalanche():
 # The test is started
    avalanchetest(20, 1000)
    avalanchetest(25, 1000)
    avalanchetest(30, 1000)
    avalanchetest(35, 1000)
    avalanchetest(40, 1000)
    avalanchetest(45, 1000)
    avalanchetest(50, 1000)
    avalanchetest(1000, 10)
    avalanchetest(5000, 10)
    avalanchetest(10000, 10)


   # avalanchetest_hash(5000, 10, True)
   # avalanchetest_hash(10000, 10, True)





def time():
 # The test is started

    en_kb, tio_kb, hundra_kb, en_mb=getFiles()
    time_adler(en_kb, tio_kb, hundra_kb, en_mb)
    time_hash(en_kb, tio_kb, hundra_kb, en_mb)




def collison_adler(str_len):
    used_values={}
    collison_counter=0
    for i in range(1000000):
        temp_str=generatestring(str_len)
        temp_hash=zlib.adler32(temp_str.encode())
        if temp_hash in used_values and temp_str!=used_values[temp_hash]:
            collison_counter+=1
        else:
            used_values[temp_hash]=temp_str

    return collison_counter


def collision_test():
    # the test is started

    print(collison(20))
    print(collison(25))
    print(collison(30))
    print(collison(35))
    print(collison(40))
    print(collison(45))
    print(collison(50))


if __name__ == '__main__':
    avalanche()
    #time()
    #collision_test()
    #avalanche()
    #test('a')
    #avalanchetest_adler(1000)
    #time_adler('aa', 'aaaa', 'aaaaaa', 'aaaaaaaa', 'aaaaaaaaaa')
   #time()