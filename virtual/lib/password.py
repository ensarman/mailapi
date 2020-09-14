import random
import string

from passlib.hash import bcrypt


def crypt_pass(raw_pass):
    """
    :param raw_pass: raw password
    :return: bcrypt password from a raw password
    """
    return '{BLF-CRYPT}' + bcrypt.using(rounds=12, ident='2y').hash(raw_pass)


def pw_gen(size=15, chars=string.ascii_letters + string.digits):
    """
    :param size: size of the password
    :param chars: complexity
    :return: random password acording the given parameters
    """
    return ''.join(random.choice(chars) for _ in range(size))
