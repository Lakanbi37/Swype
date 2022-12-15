from swype.gateways.base import SwypeBase


class Misc(SwypeBase):

    def banks(self, country="NG"):
        return self.get("/banks/%s" % country)

    def settlements(self, params):
        return self.get("/settlements", params=params)

    def get_settlement(self, id_):
        return self.get("/settlements/%s" % id_)
