"""
aaa
"""
import string
import random


_ascii_letters = string.ascii_letters
_digits = string.digits
_special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"


def generate_random_string_with_letter(length):
    """
    generate string with random length with all needed symbols

    :param length: quantity of symbols
    :return: string with symbols
    :rtype: str
    """
    return "".join(random.choice(_ascii_letters) for _ in range(length))


def generate_random_string_with_letter_and_symbol(length):
    """
    generate string with random length with all needed symbols

    :param length: quantity of symbols
    :return: string with symbols
    :rtype: str
    """
    random_string = "".join(random.choice(_ascii_letters) for _ in range(length - 1))
    random_string += random.choice(_special_chars)
    return random_string


def generate_random_string_with_letter_and_digits(length):
    """
    generate string with random length with all needed symbols and digits

    :param length: quantity of symbols
    :return: string with symbols
    :rtype: str
    """
    random_string = "".join(random.choice(_ascii_letters) for _ in range(length - 1))
    random_string += random.choice(_digits)
    return random_string
