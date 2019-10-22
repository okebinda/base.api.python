import random
import string


class String:

    @staticmethod
    def user_code(length, seed=None):
        if seed:
            random.seed(seed)

        # create initial character sequence
        chars = string.ascii_uppercase + string.digits

        # remove similar characters
        chars = chars.translate({ord(c): None for c in 'IO10'})

        # return random string
        return ''.join(random.choice(chars) for i in range(length))  # nosec
