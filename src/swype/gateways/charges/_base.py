from swype.exceptions import SwypeGatewayError
from swype.gateways.base import SwypeBase


class Charge(SwypeBase):
    path = "/charges"

    def __init__(self, _type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if _type not in ["card", "debit_ng_account", "ussd", "mpesa"]:
            raise SwypeGatewayError("Swype does not support %s charge" % _type)
        url = self.path + f"?type={_type}"
        self.path = url
        self.type = _type

    def submit(self, data: dict):
        assert isinstance(data, dict), (
            "Invalid parameters. %s expected dict got %s instead" %(self.__class__.__name__, type(data))
        )
        return self.post(self.path, data)