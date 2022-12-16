from typing import Optional, AnyStr
from dataclasses import asdict, dataclass


@dataclass(frozen=True, order=True)
class Customer:
    fullname: Optional[AnyStr]
    email: AnyStr
    phone: Optional[AnyStr]
    address: Optional[AnyStr]

    @property
    def data(self):
        return asdict(self)
