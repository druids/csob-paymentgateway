from urllib.parse import urljoin

from csob.api_response import APIResponse
from csob.exceptions import GatewaySignatureInvalid
from . import PaymentCSOBResource


class PaymentProcess(PaymentCSOBResource):
    url = 'payment/process/'
    request_signature = ('merchantId', 'payId', 'dttm')

    def get(self, key: str, pay_id: str):
        local_json = self.get_base_json()
        local_json['payId'] = pay_id
        return urljoin(self.get_url(),
                       f'{self.merchant_id}/{local_json["payId"]}/{local_json["dttm"]}/'
                       f'{self.get_url_signature(key, local_json)}')

    def parse_response_dict(self, response: dict):
        is_verified = self.verify_signature(self._gateway_key, response)
        if is_verified is False and self.raise_exception:
            raise GatewaySignatureInvalid()

        return APIResponse(is_verified=is_verified, parsed_data=response)
