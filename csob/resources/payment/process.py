from urllib.parse import urljoin

from csob.api_response import APIResponse
from csob.exceptions import GatewaySignatureInvalid
from . import PaymentCSOBResource


class PaymentProcessResource(PaymentCSOBResource):
    url = 'payment/process/'
    request_signature = ('merchantId', 'payId', 'dttm')

    def get(self, pay_id: str):
        return self._construct_url_and_get(self.get_base_json_with_pay_id(pay_id))

    def parse_response_dict(self, response: dict):
        is_verified = self.verify_signature(response)
        if is_verified is False and self.raise_exception:
            raise GatewaySignatureInvalid()

        return APIResponse(is_verified=is_verified, parsed_data=response)
