from enum import Enum

class UserRole(str, Enum):
    REALTOR = 'realtor'
    ADMIN = 'admin'
    BUYER = 'buyer'