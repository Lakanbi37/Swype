import enum
import json
import re
import typing
from swype.exceptions import CardError


class CreditCard:
    class Card(enum.StrEnum):
        VISA = "Visa"
        DINERS_CLUB = 'Diners Club'
        CHINA_UNIONPAY = 'China UnionPay'
        JCB = 'JCB'
        LASER = 'Laser'
        SOLO = 'Solo'
        SWITCH = 'Switch'
        VISA_ELECTRON = 'Visa Electron'
        MASTERCARD = 'Mastercard'
        AMEX = 'American Express'
        MAESTRO = 'Maestro'
        DISCOVER = 'Discover'

        @property
        def is_amex(self):
            return self.AMEX.value

    CARD_TYPES = [
        (Card.AMEX, (15,), ('34', '37')),
        (Card.CHINA_UNIONPAY, (16, 17, 18, 19), ('62', '88')),
        (Card.DINERS_CLUB, (14,), ('300', '301', '302', '303', '304', '305')),
        (Card.DINERS_CLUB, (14,), ('36',)),
        (Card.DISCOVER, (16,),
         list(map(str, list(range(622126, 622926))))
         + list(map(str, list(range(644, 650)))) + ['6011', '65']),
        (Card.JCB, (16,), list(map(str, list(range(3528, 3590))))),
        (Card.LASER, list(range(16, 20)), ('6304', '6706', '6771', '6709')),
        (Card.MAESTRO, list(range(12, 20)), ('5018', '5020', '5038', '5893', '6304',
                                             '6759', '6761', '6762', '6763', '0604')),
        (Card.MASTERCARD, (16,), list(map(str, list(range(51, 56))))),
        # Diners Club cards match the same pattern as Mastercard.  They are treated
        # as Mastercard normally, so we put the mastercard pattern first.
        (Card.DINERS_CLUB, (16,), ('54', '55')),
        (Card.SOLO, list(range(16, 20)), ('6334', '6767')),
        (Card.SWITCH, list(range(16, 20)), ('4903', '4905', '4911', '4936',
                                            '564182', '633110', '6333', '6759')),
        (Card.VISA, (13, 16), ('4',)),
        (Card.VISA_ELECTRON, (16,), ('4026', '417500', '4405', '4508',
                                     '4844', '4913', '4917')),
    ]

    def __init__(self, number, expiry_month, expiry_year, cvv, **kwargs):
        self._number = number
        self._expiry_month = expiry_month
        self._expiry_year = expiry_year
        self._cvv = cvv
        self._authorization: typing.Optional[typing.Dict] = None
        self._valid_cards = set(card_type[0] for card_type in self.CARD_TYPES)
        if "types" in kwargs:
            self._accepted_cards = set(kwargs.pop("types"))
            difference = self._accepted_cards - self._valid_cards
            if difference:
                raise CardError('The following accepted_cards are '
                                'unknown: %s' % difference)

    def __add__(self, other):
        assert isinstance(other, dict), "you can only add a dict instance"
        assert self.is_valid, CardError("Card data is invalid")
        data = dict(
            card_number=self._number,
            expiry_month=self._expiry_month,
            expiry_year=self._expiry_year,
            cvv=self._cvv,
            **other
        )
        if self._authorization is not None:
            data.update(dict(authorization=self._authorization))
        return json.dumps(data)

    def is_amex(self, number):
        return self.bankcard_type(number) == self.Card.AMEX

    @property
    def is_valid(self):
        """
        Check if given CC number is valid and one of the
        card types we accept
        """
        print("validating...")
        non_decimal = re.compile(r'\D+')
        number = non_decimal.sub('', (self._number or '').strip())
        if number and not self.luhn(number):
            raise CardError("Please enter a valid credit card number")
        if hasattr(self, '_accepted_cards'):
            card_type = self.bankcard_type(number)
            if card_type not in self._accepted_cards:
                raise CardError("{} cards are not accepted".format(card_type))
        # if datetime.date.month > self._expiry_month:
        #     raise CardError("Invalid expiry date")
        return True

    @property
    def _details(self):
        if self.is_valid:
            details = dict(
                expiry_month=self._expiry_month,
                expiry_year=self._expiry_year,
                card_number=self._number,
                cvv=self._cvv,
            )
            if self._authorization is not None:
                details.update(dict(authorization=self._authorization))
            return json.dumps(details)

    @staticmethod
    def matches(card_number, lengths, prefixes):
        if len(card_number) not in lengths:
            return False
        for prefix in prefixes:
            if card_number.startswith(prefix):
                return True
        return False

    def bankcard_type(self, card_number):
        """
        Return the type of bankcard based on its card_number.

        Returns None is the card_number is not recognised.
        """
        for card_type, lengths, prefixes in self.CARD_TYPES:
            if self.matches(card_number, lengths, prefixes):
                return card_type

    @staticmethod
    def luhn(card_number):
        """
        Test whether a bankcard number passes the Luhn algorithm.
        """
        card_number = str(card_number)
        sum = 0
        num_digits = len(card_number)
        odd_even = num_digits & 1

        for i in range(0, num_digits):
            digit = int(card_number[i])
            if not ((i & 1) ^ odd_even):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9
            sum = sum + digit

        return (sum % 10) == 0

    def authorize(self, data: typing.Dict):
        assert "mode" in data
        self._authorization = data

