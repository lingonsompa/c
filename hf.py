
def hash_function(input):
    # Inputen must be a string
    hash_value = 0
    for i in range(len(input)):
        hash_value = hash_value + i + ord(input[i]) * 2 ** (i)

    return hash_value % (2**32-1)


