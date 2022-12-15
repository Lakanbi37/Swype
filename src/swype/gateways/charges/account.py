from swype.gateways.charges._base import Charge
from swype.utils.generator import generate_ref


class Bank(Charge):

    """
    Flutterwave allows Nigerian merchants to charge customers bank accounts as an additional payment method.
     This makes it possible for customers to pay you through a direct bank account debit
    """

    def __init__(self, _type="debit_ng_account", *args, **kwargs):
        super().__init__(_type, *args, **kwargs)

    def initiate(self, bank, acct_no, amount, email, extra=None):
        fields, values = ["account_bank", "account_number", "amount", "email"], [bank, acct_no, amount, email]
        return self.submit(self.map_fields(fields, values, extra))

    def complete(self, otp, ref, trans_type=None):
        return super(Bank, self).complete(otp, ref, trans_type)

    def transfer(self, amount, email, currency=None, extra=None):
        if currency is None:
            currency = "NGN"
        tx_ref = generate_ref(25)
        fields, values = ["amount", "email", "currency", "tx_ref"], [amount, email, currency, tx_ref]
        params = self.map_fields(fields, values, extra)
        return self.post("/charges?type=bank_transfer", params=params)
