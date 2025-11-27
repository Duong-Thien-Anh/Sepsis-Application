import random
import string


def generate_random_string(length: int) -> str:
    """Generates a random string of a specified length using a mix of letters, digits."""
    characters = (
        string.ascii_letters + string.digits
    )

    random_string = "".join(
        random.choice(characters)
        for _ in range(length)
    )
    return random_string


def generateWithPrefix(
    prefix: str, length: int
) -> str:
    return prefix + generate_random_string(length)


def generateEmployeeCodeWithDigits(
    prefix: str, digit_length: int
) -> str:
    """Generate code with prefix + random digits only.
    Example: generateEmployeeCodeWithDigits('EMP', 7) -> 'EMP1234567' (10 chars)
    """
    digits = ''.join(str(random.randint(0, 9)) for _ in range(digit_length))
    return prefix + digits
