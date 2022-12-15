from swype.gateways.base._base import SwypeBase
from swype.gateways.bills.airtime import Airtime
from swype.gateways.bills.cable import CableTV


class BillPayment(SwypeBase):
    """

    Flutterwave allows merchants to re-sell bill payment services such as airtime payments in Nigeria, Ghana,
    and the US and DSTV payment in Nigeria and Ghana.

    Merchants get to make a 3% commission on successful Airtime sales, and a 30 naira flat commission on other bill
    services.

    To get started with our bill payment APIs you would need to follow the prerequisites below.
    """

    path = "/bills"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CableTV = CableTV(*args, **kwargs)
        self.Airtime = Airtime(*args, **kwargs)

    def pay(self, country, bill_type, recurrence, customer, amount, reference, biller):
        fields, values = ["country", "type", "customer", "amount", "reference", "recurrence", "biller_name"],\
                         [country, bill_type, customer, amount, reference, recurrence, biller]
        params = self.map_fields(fields, values)
        return self.post(self.path, params=params)

    def billers(self, params):
        assert isinstance(params, dict), (
            "Invalid query parameters passed"
        )
        return self.get("/bill-categories", params=params)
