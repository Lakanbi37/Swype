from swype.exceptions.swype_error import SwypeError


class AuthorizationError(SwypeError):
    """
    Raised when the user does not have permission to complete the requested operation.
    """
    pass
