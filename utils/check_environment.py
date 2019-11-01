import os


def is_local():
    if os.getenv('GAE_ENV', '').startswith('standard'):
        return False
    else:
        return True
