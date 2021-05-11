import string
import itertools
import timeit


def generate_strings(length=3):
    print([''.join(x) for x in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=2)])


if __name__ == '__main__':
   pass