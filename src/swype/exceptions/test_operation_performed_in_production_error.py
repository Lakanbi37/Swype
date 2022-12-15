from swype.exceptions.swype_error import SwypeError


class TestOperationPerformedInProductionError(SwypeError):
    """
    Raised when an operation that should be used for testing is used in a production environment
    """
    pass
