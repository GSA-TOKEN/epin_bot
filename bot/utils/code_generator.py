import random
import string
from typing import Optional

def generate_code(length: int = 16, prefix: Optional[str] = None) -> str:
    """Generate a random code for products"""
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    
    if prefix:
        return f"{prefix}-{code}"
    return code 