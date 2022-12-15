from swype.gateways.bills import BillPayment
from swype.gateways.charges import Bank, Card, USSD, MPESA
from swype.gateways.misc import Misc
from swype.gateways.plans import Plan
from swype.gateways.transfers import TransferBase
from swype.gateways.verification import Verification
from swype.utils.version import get_short_version, get_version
from swype.core import Swype
from swype.exceptions import ConfigurationError


class SwypeGateway:

    version = get_version()
    short_version = get_short_version()

    def __init__(self, config: Swype):
        assert isinstance(config, Swype), ConfigurationError(
            "('config') parameter not of type 'Configuration'."
            "call 'Configuration.configure()' then 'Configure.instantiate()'"
        )
        self._config = config
        self.bank = Bank(self)
        self.Card = Card(self)
        self.USSD = USSD(self)
        self.Mpesa = MPESA(self)
        self.Transfer = TransferBase(self)
        self.Plan = Plan(self)
        self.Bills = BillPayment(self)
        self.Misc = Misc(self)
        self.Verification = Verification(self)

    @property
    def config(self):
        return self._config
