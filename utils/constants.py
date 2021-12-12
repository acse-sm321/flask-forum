""" Global constants """
from enum import Enum


class UserStatus(Enum):
    """ User status """
    # Activated
    USER_ACTIVE = 1
    # Prohibited
    USER_IN_ACTIVE = 0


class UserRole(Enum):
    """ User's role """
    COMMON = 0
    ADMIN = 1
    # The root user
    SUPER_ADMIN = 2
