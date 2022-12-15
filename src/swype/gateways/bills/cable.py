from swype.gateways.bills import BillPayment
from swype.utils.generator import generate_ref


class CableTV(BillPayment):

    def connect(self, smart_card_no, amount, recurrence="ONCE", country="NG", _type="DSTV", biller=None):
        reference = generate_ref(25)
        return self.pay(
            customer=smart_card_no, 
            amount=amount, 
            recurrence=recurrence, 
            country=country, 
            bill_type=_type,
            biller=biller,
            reference=f"CAB-{reference}"
        )

    def connect_dstv(self, smart_card, amount):
        return self.connect(smart_card_no=smart_card, amount=amount)

    def auto_connect_dstv(self, smart_card_no, amount, recurrence="MONTHLY"):
        return self.connect(smart_card_no=smart_card_no, amount=amount, recurrence=recurrence)
    
    def connect_box_office(self, smart_card, amount):
        return self.connect(smart_card_no=smart_card, amount=amount, _type="DSTV BOX OFFICE")
    
    def auto_connect_box_office(self, smart_card, amount, recurrence="MONTHLY"):
        return self.connect(smart_card_no=smart_card, amount=amount, recurrence=recurrence)
