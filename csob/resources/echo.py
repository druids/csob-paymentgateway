import json
from urllib.parse import urljoin

from . import CSOBResource


class EchoResource(CSOBResource):
    url = 'echo/'
    request_signature = ('merchantId', 'dttm')
    response_signature = ('dttm', 'resultCode', 'resultMessage')

    def get(self):
        return self._construct_url_and_get(self.get_base_json())

    def post(self):
        return self._sign_and_post(self.get_base_json())
