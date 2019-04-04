from urllib.parse import urljoin

from csob.resources.payment import CSOBResource


class CustomerInfoResource(CSOBResource):
    url = 'customer/info/'
    request_signature = ('merchantId', 'customerId', 'dttm')
    response_signature = ('customerId', 'dttm', 'resultCode', 'resultMessage')

    def get(self, customer_id: str):
        local_json = self.get_base_json()

        if len(customer_id) > 50:
            raise ValueError('customerId is too long')
        local_json['customerId'] = customer_id

        return self._construct_url_and_get(local_json)
