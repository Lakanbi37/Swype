from swype.exceptions.swype_error import SwypeError


class ServerError(SwypeError):
    """
    Raised when the gateway raises an error.  Please contant support at support@getpaystack.com.

    See https://developers.paystackpayments.com/reference/general/exceptions/python#server-error
    """
    pass
