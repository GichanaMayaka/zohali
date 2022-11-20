"""
    Zohali Exceptions module
"""


class ZohaliBaseException(BaseException):
    """Base exceptions class"""


class FailedToConnectException(ZohaliBaseException):
    """Failed to connect to the network"""


class InvalidCredentialsException(ZohaliBaseException):
    """Invalid API key[s]"""
