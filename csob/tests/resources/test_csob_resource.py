import unittest

from csob.resources import CSOBResource


class TestCSOBResource(unittest.TestCase):
    class TestResource(CSOBResource):
        url = 'echo'
        request_signature = ('merchantId', 'dttm')
        response_signature = ('dttm', 'resultCode', 'resultMessage')

    def setUp(self):
        self.instance = self.TestResource(
            "https://iapi.iplatebnibrana.csob.cz/api/v1.7/",
            merchant_id="TestId",
            gateway_key="SomeKey"
        )

    def test_construct_signature_str(self):
        self.assertEqual('TestId|20190310082622',
                         self.instance._construct_signature_str({'merchantId': 'TestId', 'dttm': '20190310082622'}))

    def test_construct_verify_signature_str(self):
        self.assertEqual('20190310082622|0|OK',
                         self.instance._construct_verify_signature_str(
                             {'dttm': '20190310082622', 'resultCode': 0, 'resultMessage': 'OK'}))
