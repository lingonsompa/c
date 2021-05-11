import zlib
import random
from hf import hash_function as hash_funktion

def avalanchetest(test_len, test_range):

    counter = 0
    for j in range(test_range):
        # An original string with specified length (test_len) is created and hashed.
        # Both are converted to binary numbers. A list is created,
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
        # test with, the Hammin-distance is added to a counter. Lastly we get the average
        # distance for all new strings

        if test_len>999:

            for j in range(len(binary_list)//10):
                for i in range(0, 8):
                    new_binary = replace_bit(binary_list[10*j], i, binary_list, 10*j)
                    if new_binary:
                        temp_counter += get_dif(new_binary, old_hash_bit)
                        div += 1
            counter += temp_counter / (div)

        # The same as above, but with a new interval (all characters are replaced.

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
    # We create a string from a binary number, which is later hashed and
    # converted to a binary number. We then return the hammin-distance
    # between the hash values.

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

def generatestring(length):
 # A randomly created string with characters from chars is returned
    chars = '1234567890qwertyuiopasdfghjklzxmcnvbQWERTYUIOPASDFGHJKLZXCVBNM'
    string=''
    for i in range(length):
        string=string+chars[(random.randint(0,len(chars)-1))]
    return string


def replace_bit(binary_char, index_in_char, binary_string_list, index_in_string):
    # We replace a bit in a character that is in a specified index. If the new character is one
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

if __name__ == '__main__':
    avalanche()