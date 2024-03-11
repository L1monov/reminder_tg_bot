import string
import random


def create_token_for_rem(id_user):
    S = 20  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    ran = f"{id_user}{ran}"
    return ran

