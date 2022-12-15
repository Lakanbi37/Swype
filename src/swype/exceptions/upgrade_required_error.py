from swype.exceptions.swype_error import SwypeError


class UpgradeRequiredError(SwypeError):
    """
    Raised for unsupported client library versions.
    """
    pass
