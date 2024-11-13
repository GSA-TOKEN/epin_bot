# utils.py

import random
import string

def generate_code(length=25):
    """Generate a random code of specified length"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
