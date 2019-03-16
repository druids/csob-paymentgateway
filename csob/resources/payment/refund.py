import json
from typing import Optional

from csob.resources.payment import PaymentCSOBResource


class PaymentRefundResource(PaymentCSOBResource):
    url = 'payment/refund/'
    request_signature = ('merchantId', 'payId', 'dttm', 'amount')
    optional_request_signature = ('amount',)

    def put(self, key, pay_id: str, amount: Optional[int] = None):
        local_json = self.get_base_json()
        local_json['payId'] = pay_id
        if amount is not None:
            local_json['amount'] = amount
        local_json["signature"] = self.get_signature(key, local_json)
        return self.parse_response(self.session.post(self.get_url(), data=json.dumps(local_json)))
