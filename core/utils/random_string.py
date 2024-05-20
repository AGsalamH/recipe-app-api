'''
Generate random string of a specified length.
'''
import string
import random


def generate_random_string(length=6):
    '''Create and return random string'''
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))
