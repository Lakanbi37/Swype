from swype.exceptions.swype_error import SwypeError


class TooManyRequestsError(SwypeError):
    """
    Raised when the rate limit api threshold is exceeded.
    """
    pass
