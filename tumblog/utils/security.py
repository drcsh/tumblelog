import bcrypt


from tumblog.exceptions import security_exceptions

ENC_COST = 14
PREFIX = "2b"
PREFIX_ENCODED = b"2b"

PW_MIN_LENGTH = 6


def hash_password_string(password_str):
    """

    :param str password_str:
    :return: key
    :rtype str:
    """

    bstring = bcrypt.hashpw(password_str.encode(), bcrypt.gensalt(ENC_COST, prefix=PREFIX_ENCODED))
    return bstring.decode("utf-8")


def password_is_hashed(password):
    """
    Checks if a given string password is already hashed by bcrypt.

    According to this stack overflow (and verified in the terminal):
    https://stackoverflow.com/questions/5393803/can-someone-explain-how-bcrypt-verifies-a-hash/10933491#10933491

    Weirdly there isn't a built in for this in bcrypt.

    :param str password:
    :return: True if this looks like a bcrypt encrypted password
    :rtype bool:
    """

    return password.startswith(f'${PREFIX}${ENC_COST}') and len(password) == 60


def password_is_secure_enough(password):
    """
    Check a password meets our security requirements
    :param password:
    :return: True if it's secure 'enough'
    :raises: PasswordSecurityException if
    """

    if len(password) < PW_MIN_LENGTH:
        raise security_exceptions.PasswordSecurityException(
            f"Password is too short, must be at least {PW_MIN_LENGTH} characters."
        )

    if password.swapcase() == password:
        raise security_exceptions.PasswordSecurityException(
            "Password must contain upper and lower case characters."
        )

    # If this was a real live system, I'd be stricter and check against a password list for common passwords
    return True


def validate_password(password, hashed_password):
    """
    Check if the given str password matches the hash provided.

    :param str password:
    :param str hashed_password:
    :return:
    :rtype bool:
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
