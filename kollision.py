import zlib
import random
from hf import hash_function as hash_funktion

def generatestring(length):
 # A randomly created string with characters from chars is returned
    chars = '1234567890qwertyuiopasdfghjklzxmcnvbQWERTYUIOPASDFGHJKLZXCVBNåäöÅÄÖM'
    string=''
    for i in range(length):
        string=string+chars[(random.randint(0,len(chars)-1))]
    return string



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
    collision_test()