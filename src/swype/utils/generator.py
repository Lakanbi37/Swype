import random
import string


def generate_ref(_range=45):
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(_range))


