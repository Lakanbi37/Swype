from swype.exceptions.swype_error import SwypeError

class RequestTimeoutError(SwypeError):
    """
    Raised when a client api timeout occurs.
    """
    pass
