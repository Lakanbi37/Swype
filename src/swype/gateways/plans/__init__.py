from swype.gateways.base._base import SwypeBase
from swype.gateways.plans.subscriptions import Subscription


class Plan(SwypeBase):

    """ Flutterwave helps you collect payments recurrently from your customers using a payment plan. Payment plans
    allow you to create a subscription for your customers. When you have created a payment plan you can subscribe a
    customer to it by simply passing the plan ID in your request to charge the customers' card.

    Parameter	Required	Description

    amount	True	This is the amount for the plan. name	True	This is the name that would appear on the
    subscription reminder email interval	True	This is the charge interval e.g interval: "daily" duration
    False	This is the frequency, it is numeric, e.g. if set to 5 and intervals is set to monthly you would be
    charged 5 months, and then the subscription stops

    Case 1: if amount is not set, the amount that would be used for the plan is the amount charged from the customer
    when you start the subscription.

    Case 2: if amount is set when creating the plan, and an amount is passed when doing the subscription i.e. payment
    via the pay-button or via API calling charge endpoint. Then we charge the customer amount you passed at
    subscription as initial charge, and for subsequent charges use the amount set when creating the plan.

    Case 3: if amount is not set when creating the plan, and an amount is passed when doing the subscription i.e.
    payment via the pay-button or via API call to the charge endpoint. Then we use the amount you passed as the
    amount for the plan.

    """

    path = "/payment-plans"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Subscription = Subscription(self.gateway)

    def create(self, amount, interval, name, duration=None):
        fields, values = ["amount", "interval", "name"], [amount, interval, name]
        params = self.map_fields(fields, values)
        if duration is not None:
            params["duration"] = duration
        return self.post(self.path, params)

    def plans(self, query_params=None):
        if query_params is not None:
            assert isinstance(query_params, dict), (
                "Invalid Query Parameters. make sure you pass a dictionary"
                "as your query_params parameter"
            )
        return self.get(self.path, query_params)

    def fetch(self, plan_id):
        return self.get("%s/%s" % (self.path, plan_id))

    def update(self, plan_id, name, status):
        fields, values = list(["name", "status"]), list([name, status])
        params = self.map_fields(fields, values)
        return self.put("%s/%s" % (self.path, plan_id), params=params)

    def cancel(self, plan_id):
        return self.put("%s/%s/cancel" % (self.path, plan_id))
