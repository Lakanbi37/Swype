from swype.gateways.base._base import SwypeBase


class Verification(SwypeBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def verify_transaction(self, _id):
        return self.verify(txn_id=_id)

    def verify_account(self, acct_no, bank):
        fields, values = ["account_number", "account_bank"], [acct_no, bank]
        params = self.map_fields(fields, values)
        return self.post("/accounts/resolve", params=params)

    def verify_bvn(self, bvn):
        return self.get("/kyc/bvns/%s" % bvn)

    def resolve_card(self, pan):
        return self.get("/card-bins/%s" % pan)

