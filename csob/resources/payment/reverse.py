import json

from csob.resources.payment import PaymentCSOBResource


class PaymentReverseResource(PaymentCSOBResource):
    url = 'payment/reverse/'
    request_signature = ('merchantId', 'payId', 'dttm')

    def put(self, key, pay_id: str):
        local_json = self.get_base_json()
        local_json['payId'] = pay_id
        local_json["signature"] = self.get_signature(key, local_json)
        return self.parse_response(self.session.post(self.get_url(), data=json.dumps(local_json)))
