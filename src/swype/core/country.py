import enum


class AutoCountry(enum.Enum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


class Country(AutoCountry):
    NG = enum.auto()
    GH = enum.auto()
    KE = enum.auto()

    @property
    def nigeria(self):
        return self.NG.value

    @property
    def ghana(self):
        return self.GH.value

    @property
    def kenya(self):
        return self.KE.value
