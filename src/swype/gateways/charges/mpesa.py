from swype.gateways.charges._base import Charge
from swype.utils.generator import generate_ref


class MPESA(Charge):

    def __init__(self, _type='mpesa', *args, **kwargs):
        super().__init__(_type, *args, **kwargs)

    def initiate(self, amount: str, email: str, phone: str, extra=None):
        """
        Call this method to initiate a payment using the mpesa channel.
        pass the below parameters to the method

        After charging a customer successfully, you need to verify that the payment was successful with Flutterwave
         before giving value to your customer on your website.
        :param amount: This is the amount to be charged. It is passed in KES - ('amount':'100') - (required)
        :param email: This is the email address of the customer - (required)
        :param phone: This is the phone number linked to the customer's mobile money account - (required)
        :param extra: extra data you might want to pass down along - (optional).
        :return: {
                "status": "success",
                "message": "Charge initiated",
                "data": {
                    "id": 1191376,
                    "tx_ref": "MC-15852113s09v5050e8",
                    "flw_ref": "2899902722",
                    "device_fingerprint": "62wd23423rq324323qew1",
                    "amount": 1500,
                    "charged_amount": 1500,
                    "app_fee": 21,
                    "merchant_fee": 0,
                    "processor_response": "Successful",
                    "auth_model": "LIPA_MPESA",
                    "currency": "KES",
                    "ip": "154.123.220.1",
                    "narration": "FLW-PBF MPESA Transaction ",
                    "status": "success-pending-validation",
                    "auth_url": "N/A",
                    "payment_type": "mpesa",
                    "fraud_status": "ok",
                    "charge_type": "normal",
                    "created_at": "2020-03-27T15:46:37.000Z",
                    "account_id": 74843,
                    "customer": {
                        "id": 349271,
                        "phone_number": "25454709929220",
                        "name": "John Madakin",
                        "email": "johnmadakin@gmail.com",
                        "created_at": "2020-03-27T15:46:13.000Z"
                    }
                }
            }
        """
        fields = ["amount", "email", "phone", "currency", "tx_ref"]
        values = [amount, email, phone, "KES", generate_ref(25)]
        params = self.map_fields(fields, values, extra)
        return self.submit(params)
