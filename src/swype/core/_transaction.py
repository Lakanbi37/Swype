import json
from typing import Optional, AnyStr, Union

from swype.core._currency import Currency
from swype.core._customer import Customer
from swype.core._bank import Bank
from swype.core._creditcard import CreditCard
from swype.utils.generator import generate_ref


class Transaction:
    def __init__(self,
                 amount: int,
                 customer: Customer,
                 currency: AnyStr = Currency.ngn(),
                 bank: Optional[Bank] = None,
                 credit_card: Optional[CreditCard] = None,
                 redirect_url: Optional[AnyStr] = None
                 ):

        self._amount = amount
        self._bank = bank
        self._customer = customer
        self._currency = currency
        self._credit_card = credit_card
        self._redirect_url = redirect_url
        self._tx_ref: AnyStr = generate_ref()

    def data(self, stringify: bool = False) -> Union[str | dict]:
        payload = dict(
            amount=self._amount,
            currency=self._currency,
            tx_ref=self._tx_ref,
            **self._customer.data)
        if self._redirect_url:
            payload.setdefault("redirect_url", self._redirect_url)
        if self._credit_card:
            payload.update(**self._credit_card.data)
        if self._bank:
            payload.update(**self._bank.data)
        return json.dumps(payload) if stringify else payload

    @property
    def card(self):
        return str(self._credit_card)

    @property
    def customer(self):
        return self._customer
