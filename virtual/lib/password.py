import random
import string

from passlib.hash import bcrypt


def crypt_pass(raw_pass):
    """generate bcrypt password from a raw password"""
    return '{BLF-CRYPT}' + bcrypt.using(rounds=12, ident='2y').hash(raw_pass)


def pw_gen(size=15, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
