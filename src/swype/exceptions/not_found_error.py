from swype.exceptions.swype_error import SwypeError


class NotFoundError(SwypeError):
    """
    Raised when an object is not found in the gateway, such as a Transaction.find("bad_id").

    See https://developers.paystackpayments.com/reference/general/exceptions/python#not-found-error
    """
    pass
