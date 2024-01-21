#!/usr/bin/env python3
"""functions to encrypt passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted bcrypt hash
    """
    print(bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password matches a hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

hash_password('game')
print(is_valid(b'$2b$12$N4LWAaNVRQyr6Yz12kRrBedYbzf4RtWNwSmHI.vZTys3hgdROSmXe', "something"))
