import json
from typing import Optional

from csob.resources.payment import PaymentCSOBResource


class PaymentCloseResource(PaymentCSOBResource):
    url = 'payment/close/'
    request_signature = ('merchantId', 'payId', 'dttm', 'totalAmount')
    optional_request_signature = ('totalAmount',)

    def put(self, pay_id: str, total_amount: Optional[int] = None):
        local_json = self.get_base_json_with_pay_id(pay_id)

        if total_amount is not None:
            local_json['totalAmount'] = total_amount

        return self._sign_and_post(local_json)
