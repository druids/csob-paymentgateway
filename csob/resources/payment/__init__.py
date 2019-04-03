from typing import Dict

from csob.resources import CSOBResource


class PaymentCSOBResource(CSOBResource):
    """
    This class holds common return request signature.
    """
    response_signature = ('payId', 'dttm', 'resultCode', 'resultMessage', 'paymentStatus', 'authCode')
    optional_response_signature = ('paymentStatus', 'authCode')

    def get_base_json_with_pay_id(self, pay_id: str) -> Dict:
        """
        Call `get_base_json` and add payId to it.

        Args:
            pay_id: the payId to be added

        Returns:
            dict - json
        """
        local_json = self.get_base_json()
        local_json['payId'] = pay_id

        return local_json
