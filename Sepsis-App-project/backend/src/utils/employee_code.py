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


def generateWithPrefix(prefix: str) -> str:
    return prefix + generate_random_string(7)
