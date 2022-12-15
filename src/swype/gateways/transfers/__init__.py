from swype.gateways.base._base import SwypeBase


class TransferBase(SwypeBase):
    """" Flutterwave allows you to initiate single and bulk transfers to bank accounts and make transfers to vendors
    all from your Flutterwave account. You can either use the money you have earned as income i.e. (money collected
    from your customer's using Flutterwave) or fund your balance on Flutterwave to initiate transfers to bank
    accounts & mobile money wallets in:

    Nigeria
    Ghana
    Kenya
    Uganda
    Tanzania
    South Africa
    Zambia
    Ivory Coast
    Cameroon
    Ivory Coast
    Sierra Leone
    Burkina Faso
    Guinea Bissau
    Mali
    Senegal
    Rwanda
    Tunisia
    Guinea Conakry
    """

    path = "/transfers"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def transfer(self, bank, acct_no, amount, currency="NGN", extra=None):
        if currency == "ZAR":
            assert extra is not None and isinstance(extra, dict) and \
                   "meta" in extra and isinstance(extra["meta"], list), (
                "You have passed an invalid extra fields. "
                "please check that your extra fields is a type 'dict' and it contains"
                "a meta attribute which must be a list of objects"
            )
        fields, values = ["account_bank", "account_number", "amount", "currency"], \
                         [bank, acct_no, amount, currency]
        params = self.map_fields(fields, values, extra)
        return self.post(self.path, params)

    def retry(self, txn_id):
        return self.post(f"{self.path}/{txn_id}/retries")

    def bulk_transfer(self, data: list[dict], title=None):
        assert len(data) > 0, (
            "empty transfer data list cannot be submitted"
            "bulk data must contain at least one transfer object"
        )
        for obj in data:
            for item in ["account_bank", "account_number", "amount", "currency"]:
                assert item in obj, (
                        "you have not submitted a valid data for this bulk transfer "
                        "data at index %s is not valid. "
                        "%s is missing in data at the given index" % (data.index(obj) + 1, item)
                )
        params = dict(bulk_data=data)
        if title is not None:
            params["title"] = title
        return self.post("/bulk-transfers", params=params)

    def transfer_fee(self, amount, extra_query=None):
        fields, values = ["amount"], [amount]
        query_params = self.map_fields(fields, values, extra_query)
        return self.get("%s/fee" % self.path, params=query_params)

    def transfers(self, query_params=None):
        return self.get(self.path, query_params)

    def fetch(self, transfer_id):
        return self.get("%s/%s" % (self.path, transfer_id))

    def get_retries(self, transfer_id):
        return self.get("%s/%s/retries" % (self.path, transfer_id))

    def fetch_bulk_transfer(self, batch_id):
        query_param = dict(batch_id=batch_id)
        return self.transfers(query_param)

    def get_rates(self, amount, currency, source):
        fields, values = ["amount", "destination_currency", "source_currency"], [amount, currency, source]
        params = self.map_fields(fields, values)
        return self.config.http()._make_request("GET", "/rates", self.config.http().ContentType.json, params=params)


