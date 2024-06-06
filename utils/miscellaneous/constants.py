"""
Constants data
@Author Shidul Islam <shidul.m360ict@gmail.com>
Date: 
"""

# project info

PROJECT_NAME = "Match360"

PROJECT_URL = "https://match360.world"

PROJECT_LOGO = "https://match360.world/match_logo.png"

USER = "USER"
VENDOR = "VENDOR"
ADMIN = "ADMIN"

# Origin for cors
origins = ('http://localhost:3000',
        'http://localhost:3001',)

# Numbers for make otp
numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

# Exception types
EXCEPTION_TYPES = {
    'DEBUG': 'DEBUG',
    'INFO': 'INFO',
    'WARN': 'WARN',
    'ERROR': 'ERROR',
    'CRITICAL': 'CRITICAL'
}


# opt time minutes
EMAIL_OTP_TIME = 1

# OTP Types
VERIFY_ADMIN = 'verify_admin'
VERIFY_USER = "verify_user"
VERIFY_VENDOR = 'verify_vendor'
