from urllib.parse import urljoin

from csob.resources.payment import PaymentCSOBResource


class PaymentStatusResource(PaymentCSOBResource):
    url = 'payment/status/'
    request_signature = ('merchantId', 'payId', 'dttm')

    def get(self, key: str, pay_id: str):
        local_json = self.get_base_json()
        local_json['payId'] = pay_id
        url = urljoin(self.get_url(),
                      f'{self.merchant_id}/{local_json["payId"]}/{local_json["dttm"]}/'
                      f'{self.get_url_signature(key, local_json)}')
        return self.parse_response(self.session.get(url))
