import string
import random

from collections.abc import Iterable


def random_string(charset: Iterable = None, size: int = 8):
    if not charset:
        charset = string.ascii_letters + string.digits
    return ''.join(random.choices(charset, k=size))
