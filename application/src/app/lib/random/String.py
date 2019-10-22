import random
import string

class String(object):

    def user_code(length, seed=None):
        if seed:
            random.seed(seed)
        chars = string.ascii_uppercase + string.digits
        chars = chars.translate({ord(c): None for c in 'IO10'})  # remove similar characters
        return ''.join(random.choice(chars) for i in range(length))  # nosec
