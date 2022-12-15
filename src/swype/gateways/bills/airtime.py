from swype.gateways.bills import BillPayment
from swype.utils.generator import generate_ref


class Airtime(BillPayment):

    def buy_airtime(self, amount, phone_no, country="NG", recurrence="ONCE", biller=None):
        reference = generate_ref(25)
        return self.pay(
            amount=amount,
            country=country,
            customer=phone_no,
            reference=f"AIR-{reference}",
            recurrence=recurrence,
            biller=biller,
            bill_type="AIRTIME"
        )

    def auto_airtime(self, recurrence, amount, phone_no):
        return self.buy_airtime(recurrence=recurrence, amount=amount, phone_no=phone_no)

