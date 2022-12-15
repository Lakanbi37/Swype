from swype.gateways.charges._base import Charge
from swype.utils.generator import generate_ref


class USSD(Charge):

    """
    Flutterwave allows you to collect payments from your customers offline using USSD. With USSD payments,
     you call our APIs to create a charge, then give your customer instructions to complete the
     payment on her/his mobile phone. Once payment is completed we notify you on your webhook.

    At the moment, banks available for USSD payments (and their numeric codes) are:
    Fidelity Bank -- (070),
    Guaranty Trust Bank -- (058),
    Keystone Bank -- (082),
    Sterling Bank -- (232),
    United Bank for Africa -- (033),
    Unity Bank -- (215), and
    Zenith Bank -- (057).]

    When you call the initiate method you would receive the JSON response above with a note field that contains
    the USSD code for your customer to dial to complete their payment.
    Then we call your webhook once the transaction has been completed with a successful response.
    """

    def __init__(self, _type="ussd", *args, **kwargs):
        super().__init__(_type, *args, **kwargs)

    def initiate(self, bank, amount, email, currency=None, extra=None):
        """
        sample request
        {
            "tx_ref": "MC-15852309v5050e8",
            "account_bank": "058",
            "amount": "1500",
            "currency": "ZMW",
            "email": "user@gmail.com",
            "phone_number": "054709929220",
            "fullname": "John Madakin",
        }
        :param bank: This is the Bank numeric code - e.g 058
        :param amount: This is the amount to be charged. It is passed in NGN - ('amount':'1500').
        :param email: This is the email address of the customer.
        :param currency: defaults to 'NGN' if not currency was passed
        :param extra: extra data to be passed to this  transaction - optional
        :return: {
                    "status": "success",
                    "message": "Charge initiated",
                    "data": {
                        "id": 276641033,
                        "tx_ref": "ussd-payment",
                        "flw_ref": "FLW693741590884271975",
                        "device_fingerprint": "N/A",
                        "amount": 300,
                        "charged_amount": 300,
                        "app_fee": 4.2,
                        "merchant_fee": 0,
                        "processor_response": "Transaction in progress",
                        "auth_model": "USSD",
                        "currency": "NGN",
                        "ip": "::ffff:10.143.30.109",
                        "narration": "John Madakin",
                        "status": "pending",
                        "payment_type": "ussd",
                        "fraud_status": "ok",
                        "charge_type": "normal",
                        "created_at": "2020-05-31T00:17:51.000Z",
                        "account_id": 17321,
                        "customer": {
                            "id": 210466255,
                            "phone_number": "07033950328",
                            "name": "John Madakin",
                            "email": "user@gmail.com",
                            "created_at": "2020-05-31T00:17:50.000Z"
                        },
                        "payment_code": "9039"
                    },
                    "meta": {
                        "authorization": {
                            "mode": "ussd",
                            "note": "*bank_ussd_code*000*9039#"
                        }
                    }
                }
        """
        if currency is None:
            currency = "NGN"
        txn_ref = generate_ref(25)
        fields, values = ["account_bank", "amount", "email", "currency", "tx_ref"],\
                         [bank, amount, email, currency, txn_ref]
        params = self.map_fields(fields, values, extra)
        return self.submit(params)



