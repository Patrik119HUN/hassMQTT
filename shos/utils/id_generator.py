import random
import string


def generate_id(length: int = 8) -> str: return "".join(
    random.choices(string.ascii_lowercase + string.digits, k=length))
