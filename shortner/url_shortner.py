#!/usr/bin/python3
"""Creates a url shortner using an algorithm and generating unque id
for the long url
"""


import hashlib
import random
import string


def base62_encode(hash_int):
    """Implementation of base62 encoding
    """
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    temp_list = []

    while hash_int > 0:
        hash_int, r = divmod(hash_int, 62)
        temp_list.append(chars[r])

    return ''.join(reversed(temp_list))


def url_shortner(original):
    """Creates algoorithm to use
    """

    # url = input("Enter url: ")
    sha_hash = hashlib.sha256(original.encode()).hexdigest()
    hash_int = int(sha_hash, 16)  # convert the hex hash to an integer
    short_code = base62_encode(hash_int)
    # print(short_code)
    result = short_code[:7]
    # print(result)
    return result
    """if database has result:
        result = short_code[-7:]"""


def generate_random_url(length=0):
    """Serves as helper to url_shortner. If the shortened url
    exists in the database this function would be called to
    generate a new url
    """
    if length > 1:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    else:
        return generate_random_url(6)


if __name__ == '__main__':
    url_shortner()
