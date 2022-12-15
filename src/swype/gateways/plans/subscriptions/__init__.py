from swype.gateways.base._base import SwypeBase


class Subscription(SwypeBase):
    path = "/subscriptions"

    def subscriptions(self, query_params=None):
        if query_params is not None:
            assert isinstance(query_params, dict), (
                "Invalid Query Parameters. make sure you pass a dictionary"
                "as your query_params parameter"
            )
        return self.get(self.path, query_params)

    def cancel(self, sub_id):
        return self.put("%s/%s/cancel" % (self.path, sub_id))

    def activate(self, sub_id):
        return self.put("%s/%s/activate" % (self.path, sub_id))
