import string
import random

_ascii_letters = string.ascii_letters
_digits = string.digits
_special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~ "


def generate_random_string(length):
    """
    Generate a random string with the given length using ASCII letters.

    :param length: Length of the string to generate.
    :return: Random string.
    """
    return "".join(random.choice(_ascii_letters) for _ in range(length))


def add_special_character(func):
    """
    Decorator function to add a special character to the end of the generated string.
    """
    def wrapper(length):
        random_string = func(length - 1)
        random_string += random.choice(_special_chars)
        return random_string
    return wrapper


def add_digit(func):
    """
    Decorator function to add a digit to the end of the generated string.
    """
    def wrapper(length):
        random_string = func(length - 1)
        random_string += random.choice(_digits)
        return random_string
    return wrapper


def add_digit_and_special_character(func):
    """
    Decorator function to add a digit to the end of the generated string.
    """
    def wrapper(length):
        random_string = func(length-2)
        random_string += random.choice(_digits)
        random_string += random.choice(_special_chars)
        return random_string
    return wrapper


def add_hyphen(func):
    """
    Decorator function to add a hyphen to the end of the generated string.
    """
    def wrapper(length):
        random_string = func(length - 1)
        random_string += "-"
        return random_string
    return wrapper


@add_special_character
def generate_random_string_with_symbol(length):
    """
    Generate a random string with the given length using ASCII letters and add a special character at the end.

    :param length: Length of the string to generate.
    :return: Random string with a special character.
    """
    return generate_random_string(length)


@add_hyphen
def generate_random_string_with_hyphen(length):
    """
    Generate a random string with the given length using ASCII letters and add a hyphen at the end.

    :param length: Length of the string to generate.
    :return: Random string with a special character.
    """
    return generate_random_string(length)


@add_digit
def generate_random_string_with_digits(length):
    """
    Generate a random string with the given length using ASCII letters and add a digit at the end.

    :param length: Length of the string to generate.
    :return: Random string with a digit.
    """
    return generate_random_string(length)


@add_digit_and_special_character
def generate_random_string_with_digits_and_symbols(length):
    """
    Generate a random string with the given length using ASCII letters, add a digit and symbol.

    :param length: Length of the string to generate.
    :return: Random string with a digit.
    """
    return generate_random_string(length)


def generate_random_bool():
    """
    Generate a random boolean value

    :return: True || False
    """
    return random.choice([True, False])


def generate_random_integer():
    """
    Generate a random integer value

    :return: random integer value
    """
    return random.randint(0, 10000)
