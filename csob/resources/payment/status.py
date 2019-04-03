from urllib.parse import urljoin

from csob.resources.payment import PaymentCSOBResource


class PaymentStatusResource(PaymentCSOBResource):
    url = 'payment/status/'
    request_signature = ('merchantId', 'payId', 'dttm')

    def get(self, pay_id: str):
        return self._construct_url_and_get(self.get_base_json_with_pay_id(pay_id))
