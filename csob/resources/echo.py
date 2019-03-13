import json as json
from urllib.parse import urljoin

from . import CSOBResource


class EchoResource(CSOBResource):
    url = 'echo'
    request_signature = ('merchantId', 'dttm')
    response_signature = ('dttm', 'resultCode', 'resultMessage')

    def get(self, key):
        local_json = self.get_base_json()
        url = urljoin(self.get_url(),
                      f'{self.merchant_id}/{local_json["dttm"]}/{self.get_url_signature(key, local_json)}')
        return self.parse_response(self.session.get(url))

    def post(self, key):
        local_json = self.get_base_json()
        local_json["signature"] = self.get_signature(key, local_json)
        return self.parse_response(self.session.post(self.get_url(), data=json.dumps(local_json)))
