import dataclasses
from typing import AnyStr


@dataclasses.dataclass(frozen=True, order=True)
class Bank:
    account_number: AnyStr
    account_bank: AnyStr

    @property
    def data(self):
        return dict(account_number=self.account_number, account_bank=self.account_bank)
