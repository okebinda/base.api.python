"""
Random library.

Generate random strings for specific purposes.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=too-few-public-methods

import random
import string


class String:
    """Helper for random string values"""

    @staticmethod
    def user_code(length, seed=None):
        """Generates a random string of uppercase letters + digits

        Creates a random string from uppercase characters and digits. Removes
        certain characters that are easily confused for each other, such as
        'O' and '0'. This is intended to be used for user-facing, one-time
        codes such as for password reset requests, and is not considered
        cryptographically secure.

        :param length: Length of string to generate
        :type length: int
        :param seed: Random seed
        :return: Random user code
        :rtype: str
        """

        if seed:
            random.seed(seed)

        # create initial character sequence
        chars = string.ascii_uppercase + string.digits

        # remove similar characters
        chars = chars.translate({ord(c): None for c in 'IO10'})

        # return random string
        return ''.join(random.choice(chars) for i in range(length))  # nosec
