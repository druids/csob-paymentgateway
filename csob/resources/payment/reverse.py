import json

from csob.resources.payment import PaymentCSOBResource


class PaymentReverseResource(PaymentCSOBResource):
    url = 'payment/reverse/'
    request_signature = ('merchantId', 'payId', 'dttm')

    def put(self, pay_id: str):
        return self._sign_and_put(self.get_base_json_with_pay_id(pay_id))
