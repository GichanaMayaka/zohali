class ZohaliException(Exception):
    """Base exception class"""
    pass


class FailedAuthenticationError(ZohaliException):
    """Raised when authentication status fails"""
    pass
