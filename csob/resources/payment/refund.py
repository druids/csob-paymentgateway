import json
from typing import Optional

from csob.resources.payment import PaymentCSOBResource


class PaymentRefundResource(PaymentCSOBResource):
    url = 'payment/refund/'
    request_signature = ('merchantId', 'payId', 'dttm', 'amount')
    optional_request_signature = ('amount',)

    def put(self, pay_id: str, amount: Optional[int] = None):
        local_json = self.get_base_json_with_pay_id(pay_id)

        if amount is not None:
            local_json['amount'] = amount

        return self._sign_and_put(local_json)
