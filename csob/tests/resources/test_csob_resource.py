import unittest

from csob.resources import CSOBResource
from csob.tests.resources import get_private_key, get_gateway_key


class TestCSOBResource(unittest.TestCase):
    class TestResource(CSOBResource):
        url = 'echo'
        request_signature = ('merchantId', 'dttm')
        response_signature = ('dttm', 'resultCode', 'resultMessage')

    def setUp(self):
        self.instance = self.TestResource(
            private_key=get_private_key(),
            base_url="https://iapi.iplatebnibrana.csob.cz/api/v1.7/",
            merchant_id="TestId",
            gateway_key=get_gateway_key()
        )

    def test_construct_signature_str(self):
        self.assertEqual('TestId|20190310082622',
                         self.instance._construct_signature_str({'merchantId': 'TestId', 'dttm': '20190310082622'}))

    def test_construct_signature_str_with_dict(self):
        self.assertEqual('Test|Id|20190310082622',
                         self.instance._construct_signature_str(
                             {'merchantId': [{'id': 'Test', 'name': 'Id'}], 'dttm': '20190310082622'}))

    def test_construct_verify_signature_str(self):
        self.assertEqual('20190310082622|0|OK',
                         self.instance._construct_verify_signature_str(
                             {'dttm': '20190310082622', 'resultCode': 0, 'resultMessage': 'OK'}))

    def test_get_url_args(self):
        self.assertEqual(('merchantId', 'dttm', 'signature'), self.instance.get_url_args())

    def test_construct_url(self):
        local_json = {'merchantId': 'TestId', 'dttm': '20190310082622'}
        self.assertEqual(
            'https://iapi.iplatebnibrana.csob.cz/api/v1.7/TestId/20190310082622/DvxWQKW782%2FP%2FGoPoFWzWJtvZ3sTuI7Lzfl'
            'kZT3jvWd8nDNHxYItRqefR%2FQI3qX2EYJICcHopMRLJbIisblLXzpylA7BoVhSFkiiF05t3R0GqoXTnIkrFsAiZStqHAeQ%2BIaIH2wJF'
            'H8aLzFPWy7yu0kJ0z9xVfilETN687mE7oOknrsSIQCXYfPUcku1ApKYuZpCekezcg1NdrXX7VasCnofZ2AcTOU6umS4Mi%2F8LrW7TFzY4'
            'YC5ukQUVaF6hfQMIGvh8Sm479VtoTdWTGP7jl%2FANw5K%2Bq%2FpDgk4W1SB4cLi5Jb2CXQJfy2TGIHyoSHdGFRo1%2FugwmjnJC0HLFs'
            'ftA%3D%3D',
            self.instance.construct_url(local_json))
