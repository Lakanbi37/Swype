from swype import gateways
from swype.exceptions.invalid_parameter import InvalidParameters


class SwypeBase:
    path = ""

    def __init__(self, gateway: gateways.SwypeGateway):
        if not isinstance(gateway, gateways.SwypeGateway):
            raise InvalidParameters("%s class gateway parameter must be a SwypeGateway instance"
                                    % self.__class__.__name__)
        self._config = gateway.config

    def post(self, url, params=None):
        params = dict() if params is None else params
        return self._config._http().post(url, params) # NOQA

    def get(self, url, params=None):
        params = dict() if params is None else params
        return self._config._http().get(url, params) # NOQA

    def put(self, url, params):
        return self._config._http().put(url, params) # NOQA

    def patch(self, url, params):
        return self._config._http().patch(url, params) # NOQA

    def delete(self, url):
        return self._config._http().delete(url) # NOQA

    def verify(self, txn_id):
        """
        After charging a customer successfully, you need to verify that the payment was successful with Flutterwave
        before giving value to your customer on your website. To do so, call our verify transactions endpoint
        /transactions/:id/verify with your transaction ID transaction_id to ensure that the transaction went through
        successfully with Flutterwave. More on how to verify transactions Transaction verification

        Although the Flutterwave inline already verifies the payment from the client-side, we strongly recommend you
        still do a server-side verification to be double sure no foul play occurred during the payment flow.

        Below are the important things to check for in the response object when validating the payment:

        Verify the transaction reference.

        Verify the data.status of the transaction to be successful.

        Verify the currency to be the expected currency

        Most importantly validate the amount paid to be equal to or at least greater than the amount of the value to
        be given.
        :param txn_id: the transaction id
        :return: {
                "status": "success",
                "message": "Transaction fetched successfully",
                "data": {
                    "id": 288200108,
                    "tx_ref": "LiveCardTest",
                    "flw_ref": "YemiDesola/FLW275407301",
                    "device_fingerprint": "N/A",
                    "amount": 100,
                    "currency": "NGN",
                    "charged_amount": 100,
                    "app_fee": 1.4,
                    "merchant_fee": 0,
                    "processor_response": "Approved by Financial Institution",
                    "auth_model": "PIN",
                    "ip": "::ffff:10.5.179.3",
                    "narration": "CARD Transaction ",
                    "status": "successful",
                    "payment_type": "card",
                    "created_at": "2020-07-15T14:31:16.000Z",
                    "account_id": 17321,
                    "card": {
                        "first_6digits": "232343",
                        "last_4digits": "4567",
                        "issuer": "FIRST CITY MONUMENT BANK PLC",
                        "country": "NIGERIA NG",
                        "type": "VERVE",
                        "token": "flw-t1nf-4676a40c7ddf5f12scr432aa12d471973-k3n",
                        "expiry": "02/23"
                    },
                    "meta": null,
                    "amount_settled": 98.6,
                    "customer": {
                        "id": 216519823,
                        "name": "Yemi Desola",
                        "phone_number": "N/A",
                        "email": "user@gmail.com",
                        "created_at": "2020-07-15T14:31:15.000Z"
                    }
                }
            }
        """
        return self.get(f"/transaction/{txn_id}/verify")

    def complete(self, otp, ref, trans_type=None):
        data = dict(otp=otp, flw_ref=ref)
        if trans_type is not None:
            data["type"] = trans_type
        return self.post("/validate-charge", data)

    def refund(self, txn_id, amount):
        return self.post("/transactions/%s/refund" % txn_id, params=dict(amount=amount))

    def trans_timeline(self, txn_id):
        return self.get("/transactions/%s/events" % txn_id)

    def transactions(self, query_params):
        return self.get("/transactions", params=dict(**query_params))

    def get_fee(self, query_params):
        return self.get("/transactions/fee", params=dict(**query_params))

    def map_fields(self, fields: list[str], values: list, extra: dict = None) -> dict:
        assert len(fields) == len(values), (
                "%s many have a missing field"
                "Check your data then try again"
                % self.__class__.__name__
        )
        payload = dict(zip(fields, values))
        if extra is not None:
            assert isinstance(extra, dict), (
                "Extra data is required to be a dictionary"
            )
            for key in extra.keys():
                assert key not in payload, (
                        "%s field cannot override default values. "
                        "kindly remove from the extra object"
                        "or change its default value"
                        % key
                )
            payload.update(extra)
        return payload

    @property
    def config(self):
        return self._config
