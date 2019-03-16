import json
from typing import Optional

from csob.resources.payment import PaymentCSOBResource


class PaymentCloseResource(PaymentCSOBResource):
    url = 'payment/close/'
    request_signature = ('merchantId', 'payId', 'dttm', 'totalAmount')
    optional_request_signature = ('totalAmount',)

    def put(self, key, pay_id: str, total_amount: Optional[int] = None):
        local_json = self.get_base_json()
        local_json['payId'] = pay_id
        if total_amount is not None:
            local_json['totalAmount'] = total_amount
        local_json["signature"] = self.get_signature(key, local_json)
        return self.parse_response(self.session.post(self.get_url(), data=json.dumps(local_json)))
