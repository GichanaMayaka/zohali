class ZohaliException(Exception):
    """Base exception class"""
    pass


class FailedAuthenticationError(ZohaliException):
    """Raised when authentication status fails"""
    pass


class NoTweetsException(ZohaliException):
    """Raised when no tweet is found"""
    pass
