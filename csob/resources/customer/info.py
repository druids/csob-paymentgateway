from urllib.parse import urljoin

from csob.resources.payment import CSOBResource


class CustomerInfoResource(CSOBResource):
    url = 'customer/info/'
    request_signature = ('merchantId', 'dttm')
    response_signature = ('customerId', 'dttm', 'resultCode', 'resultMessage')

    def get(self, key, customer_id: str):
        local_json = self.get_base_json()

        if len(customer_id) > 50:
            raise ValueError('customerId is too long')
        local_json['customerId'] = customer_id
        url = urljoin(self.get_url(),
                      f'{self.merchant_id}/{local_json["customerId"]}/{local_json["dttm"]}'
                      f'/{self.get_url_signature(key, local_json)}')
        return self.parse_response(self.session.get(url))
