from typing import Optional, AnyStr, Dict

from swype.core import Currency, Transaction
from swype.exceptions import TransactionError
from swype.exceptions.upgrade_required_error import UpgradeRequiredError
from swype.gateways.charges._base import Charge
from swype.utils.generator import generate_ref


class Card(Charge):
    """
    Flutterwave allows you to charge both local cards (issued in your country of operations) and International cards
    using our APIs. When charging cards with Flutterwave, you have to take card authentication methods into account.
    This is primarily how the user who is meant to pay you authenticates their transaction e.g. using a one time pin
    (OTP), a card internet PIN (i-Pin), or an address verification system (AVS) or without any authentication set.

    We automatically detect the authentication model to be used by the card and send a response requiring you to pass
    the needed parameter for that authentication model.

    Step 1 - Collect payment details from customer You can use a custom form to collect the card details from the
    customer including any extra information needed, see a sample of the card details to collect from the customer. {
    "card_number":"4556052704172643", "cvv":"899", "expiry_month":"01", "expiry_year":"21", "currency":"NGN",
    "amount":"1000", "email":"user@gmail.com", "fullname":"yemi desola", "tx_ref":"MC-3243e",
    "redirect_url":"https://webhook.site/3ed41e38-2c79-4c79-b455-97398730866c" }

    Step 2 - Encrypt payment details To see how to encrypt using any of our encryption functions copy the sample
    request above and visit the Flutterwave Encryption section. If you handle your encryption well, you should
    receive an encrypted payload like the one below:

    data = { "client": "Rd8k8kDWguht2vKTq3fy4InO8JjaYVXSIBEioVRIJta6EmdhI5Z
    /9VRpTw88inynsfcsa76fZd4pjvt2kwx8JaWWjHPmXx02Apsl7SgzRLcK48su4zcCpmJFcX1YQHnIJa36T4KC0/JVd0GUD/m9d6N/D
    /RKSJTDbBnfj6hI9c9UaU1AmnFj3vmhq0/eyH56rjqOB2ryS9lr37Tb0ZttMPjfTQl7ziZwUksb0tC2XHeQaDM+SNCAZAAwE1CfLh2RXCTzGXg6F
    +basDvg4yT8XtvkaQKN33no1X+jCBL2Pc7ub8RmL9Hvc
    +8th7XF8Ye0eTElolaGlhuFAIcn0yL3B5JZ2eAoNevp0dDmqMdQi9qY6QJRUK3pVOW11u5qsLnB3flQtshB7V4v9fgzN4qCE7+emacE6pbwg
    +7aHQICykf69p2DtZTmZvK9CpVrtYSA5PABX/TV8Vw=" }
    You can then use this payload to initiate payment

    Step 3 - Initiate payment
    call the initiate() method of this class and pass in your encrypted client data - e.g
    wave.Card.initiate(data["client"]) - the initiate method accepts a string object not a dictionary

    Payment Responses
    When you initiate the payment you would get a response based on the type of card that was sent
    to Flutterwave, we'll explain the response you would get for each card type and what you need to do next for each
    of the card types.

    1. Using a Nigerian Issued Mastercard / Verve card
    When your customer is paying with a Nigerian MasterCard/Verve
    card, we suggest that you charge the card using the customer's PIN, the suggested authorization mode is returned
    after initiating payment, you would get a response that looks like this:
    {
       "status":"success",
       "message":"Charge authorization data required",
       "meta":{
          "authorization":{
             "mode":"pin",
             "fields":[
                "pin"
             ]
          }
       }
    }

    This response tells you that the authentication model for the card is PIN. What you need to do next is add an
    authorization object containing the cards authorization mode i.e pin and the card's pin to your initial payload,
    re-encrypt it and call the authenticate method of this class passing the encrypted string as a parameter. you'll get
    a response which looks like this
    {
    "status": "success",
    "message": "Charge initiated",
    "data": {
            "id": 288192886,
            "tx_ref": "LiveCardTest",
            "flw_ref": "YemiDesola/FLW275389391",
            "device_fingerprint": "N/A",
            "amount": 100,
            "charged_amount": 100,
            "app_fee": 1.4,
            "merchant_fee": 0,
            "processor_response": "Kindly enter the OTP sent to *******0328",
            "auth_model": "PIN",
            "currency": "NGN",
            "ip": "::ffff:10.7.214.204",
            "narration": "CARD Transaction ",
            "status": "pending",
            "auth_url": "N/A",
            "payment_type": "card",
            "fraud_status": "ok",
            "charge_type": "normal",
            "created_at": "2020-07-15T14:06:55.000Z",
            "account_id": 17321,
            "customer": {
                "id": 216517630,
                "phone_number": null,
                "name": "Yemi Desola",
                "email": "usef@gmail.com",
                "created_at": "2020-07-15T14:06:55.000Z"
            },
            "card": {
                "first_6digits": "123456",
                "last_4digits": "2343",
                "issuer": "MASTERCARD GUARANTY TRUST BANK Mastercard Naira Debit Card",
                "country": "NG",
                "type": "MASTERCARD",
                "expiry": "08/22"
            }
        },
        "meta": {
            "authorization": {
                "mode": "otp",
                "endpoint": "/v3/validate-charge"
            }
        }
    }

    Validate transactions
    At this point, two things are to be expected, depending on the type of card you're charging.

    A redirect link will be returned with a processor_response message saying Pending Validation. In this case,
    you only need to redirect your customers to the returned link where they can complete the payment. You can check the
    3DS Auth model section further down on this page for more guides on how to complete this process.

    An OTP will be sent to your customer for validation. This is the case for the response we have above.

    In the charge response above, processor_response contains the instructions on how to complete this transaction
    using the OTP sent to the card owner. To validate the transaction, call our validate() or complete() method with the
    customer's OTP and pass the flw_ref in the request body. you would receive a response which looks like
    {
        "status": "success",
        "message": "Charge validated",
        "data": {
            "id": 288200108,
            "tx_ref": "LiveCardTest",
            "flw_ref": "YemiDesola/FLW275407301",
            "device_fingerprint": "N/A",
            "amount": 100,
            "charged_amount": 100,
            "app_fee": 1.4,
            "merchant_fee": 0,
            "processor_response": "Approved by Financial Institution",
            "auth_model": "PIN",
            "currency": "NGN",
            "ip": "::ffff:10.5.179.3",
            "narration": "CARD Transaction ",
            "status": "successful",
            "auth_url": "N/A",
            "payment_type": "card",
            "fraud_status": "ok",
            "charge_type": "normal",
            "created_at": "2020-07-15T14:31:16.000Z",
            "account_id": 17321,
            "customer": {
                "id": 216519823,
                "phone_number": null,
                "name": "Yemi Desola",
                "email": "user@gmail.com",
                "created_at": "2020-07-15T14:31:15.000Z"
            },
            "card": {
                "first_6digits": "232343",
                "last_4digits": "4567",
                "issuer": "VERVE FIRST CITY MONUMENT BANK PLC",
                "country": "NG",
                "type": "VERVE",
                "expiry": "03/23"
            }
        }
    }

    """

    def __init__(self, _type="card", *args, **kwargs):
        super().__init__(_type, *args, **kwargs)
        self._transaction: Optional[Transaction] = None

    def initiate(self, transaction: Transaction):
        """
        Collect payment details from customer You can use a custom form to collect the card details from the
        customer including any extra information needed, see a sample of the card details to collect from the customer. {
        "card_number":"4556052704172643", "cvv":"899", "expiry_month":"01", "expiry_year":"21", "currency":"NGN",
        "amount":"1000", "email":"user@gmail.com", "fullname":"yemi desola", "tx_ref":"MC-3243e",
        "redirect_url":"https://webhook.site/3ed41e38-2c79-4c79-b455-97398730866c" }
        """
        self._transaction = transaction
        data = self._transaction.data(stringify=True)
        assert isinstance(data, str), TransactionError("Transaction data must be string")
        client = self.config.encrypt(data)
        return self._initiate(client)

    def _initiate(self, client):
        assert isinstance(client, str), (
                "'%s' card holder data must be an encrypted string"
                "transmission of naked card holder is forbidden"
                % self.__class__.__name__
        )
        fields, values = ["client"], [client]
        return self.submit(self.map_fields(fields, values))

    def authenticate(self, authorization: Dict):
        self._transaction.card.authorize(authorization)
        data = self._transaction.data(stringify=True)
        assert isinstance(data, str), TransactionError("Transaction data must be string")
        client = self.config.encrypt(data)
        return self._initiate(client)

    def validate(self, otp, ref, txn_type=None):
        return self.complete(otp, ref, txn_type)

    def verify(self, txn_id):
        return super(Card, self).verify(txn_id)

    def capture(self, ref, amount):
        data = dict(amount=amount)
        return self.post("/charges/%s/capture" % ref, data)

    def void(self, ref: str):
        return self.post("/charges/%s/void" % ref)

    def authorize(self,
                  token,
                  amount,
                  email,
                  currency: Optional[AnyStr] = Currency.ngn(),
                  country=None, extra=None):
        """
        Create a tokenized charge
        :param token: This is the card token returned from the transaction verification
        endpoint as data.card.token
        :param amount: This is the amount to be charged
        :param email: This is the email
        address of the customer. Note: This has to be the exact email address passed during the initial charge
        :param currency: This is the specified currency to charge the card in,
                            It can be NGN, GHS, KES, UGX, TZS, USD etc.
        :param country: This is the ISO country code of the merchant e.g. NG, GH, KE etc.
        :param extra: extra data you might want to pass down
        :return: {
                   "status":"success",
                   "message":"Charge successful",
                   "data":{
                      "id":277036749,
                      "tx_ref":"new-live-test",
                      "flw_ref":"FLW253481676",
                      "redirect_url":"http://127.0.0",
                      "device_fingerprint":"N/A",
                      "amount":300,
                      "charged_amount":300,
                      "app_fee":4.2,
                      "merchant_fee":0,
                      "processor_response":"APPROVED",
                      "auth_model":"noauth",
                      "currency":"NGN",
                      "ip":"123.456.543",
                      "narration":"pstmn charge",
                      "status":"successful",
                      "payment_type":"card",
                      "created_at":"2020-06-01T01:31:59.000Z",
                      "account_id":17321,
                      "customer":{
                         "id":210745229,
                         "phone_number":null,
                         "name":"Yemi Desola",
                         "email":"user@gmail.com",
                         "created_at":"2020-06-01T01:27:24.000Z"
                      },
                      "card":{
                         "first_6digits":"123456",
                         "last_4digits":"7890",
                         "issuer":"MASTERCARD GUARANTY TRUST BANK Mastercard Naira Debit Card",
                         "country":"NG",
                         "type":"MASTERCARD",
                         "expiry":"08/22",
                         "token":"flw-t1nf-f9b3bf384cd30d6fca42b6df9d27bd2f-m03k"
                      }
                   }
                }
        """
        if not country:
            country = "NG"
        tx_ref = generate_ref(25)
        fields, values = ["token", "amount", "email", "currency", "country", "tx_ref"], \
            [token, amount, email, currency, country, tx_ref]
        params = self.map_fields(fields, values, extra)
        return self.post("/tokenized-charges", params=params)

    def update_card_info(self, token, first_name, last_name, email, phone_number):
        """
        Update details tied to a customer card token
        :param token: This is the card token returned from the transaction verification endpoint as data.card.token
        :param first_name: This the customer's first name you want to attach to the token
        :param last_name: This the customer's last name you want to attach to the token
        :param email: The new email you would like to attach to the token.
        :param phone_number: This is the customer's phone number you want to attach to this token
        :return: {
            "status": "success",
            "message": "Token details updated",
            "data": {
                "email": "ken@example.com",
                "fullname": "Kendrick Graham",
                "phone_number": "0813XXXXXX22",
                "created_at": "2020-06-11T16:25:44.000Z"
            }
        }
        """
        fields, values = ["email", "first_name", "last_name", "phone_number"], \
            [email, first_name, last_name, phone_number]
        params = self.map_fields(fields, values)
        return self.post("/tokens/%s" % token, params=params)

    def bulk_authorize(self, params):
        raise UpgradeRequiredError("This function is not available on this version")

    def refund_capture(self, ref, amount):
        return self.post("/charges/%s/capture" % ref, params=dict(amount=amount))
