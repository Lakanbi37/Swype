import enum


class AutoName(enum.Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


@enum.unique
class Currency(AutoName):
    USD = enum.auto()
    NGN = enum.auto()
    GHS = enum.auto()
    KES = enum.auto()
    UGX = enum.auto()
    TZS = enum.auto()
    GBP = enum.auto()

    @classmethod
    def usd(cls):
        return cls.USD.value

    @classmethod
    def ngn(cls):
        return cls.NGN.value

    @classmethod
    def ghs(cls):
        return cls.GHS.value

    @classmethod
    def kes(cls):
        return cls.KES.value

    @classmethod
    def ugx(cls):
        return cls.UGX.value

    @classmethod
    def tzs(cls):
        return cls.TZS.value

    @classmethod
    def gbp(cls):
        return cls.GBP.value
