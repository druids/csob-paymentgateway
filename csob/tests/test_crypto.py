import os
import sys
import unittest

from csob.crypto import get_signature, get_url_signature, verify_signature


class TestSinging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(sys.prefix, "csob_keys/rsa_test_A3746UdxZO.key")) as f:
            cls.key = f.read()

    def test_get_signature(self):
        signature_str = 'A3746UdxZO|20190312143240'
        expected_output = (
            'JOZUX9wUlzFqbSbrUbLZLufzJEhaxiu2pGY1skck9mQNkS3x4TawieMFBiyeayBlOQF4i5074gO4kUg6rlCF5RAYfm'
            'RjhIXsqviEzOIYt/hZ1mIaEUWVZI/ABxh4BSMUwKqzCjMitiYf/VbqIzfD5FjZtjbE2A+SSy9hAlvmyqQqZur3czrn'
            'YGVhmLChzurPaOvitOsXq5FyZGy7vQPI7jzhrO7GRpm0t7DFDkzWm3R3vR6T159SCESvQHLoUkv7kqswDkBiW+jqk8'
            'rRlO9p20ZsqzcxyJcls4flhzczyBRA8YNu6N6gb+ylV12CasXcEYA/4owOfeWtWHR7YxLfIA=='
        )

        self.assertEqual(get_signature(self.key, signature_str), expected_output)

    def test_get_url_signature(self):
        signature_str = 'A3746UdxZO|20190312143240'
        expected_output = (
            'JOZUX9wUlzFqbSbrUbLZLufzJEhaxiu2pGY1skck9mQNkS3x4TawieMFBiyeayBlOQF4i5074gO4kUg6rlCF5RAYfmRjhIXsqviEzOIY'
            't%2FhZ1mIaEUWVZI%2FABxh4BSMUwKqzCjMitiYf%2FVbqIzfD5FjZtjbE2A%2BSSy9hAlvmyqQqZur3czrnYGVhmLChzurPaOvitOsX'
            'q5FyZGy7vQPI7jzhrO7GRpm0t7DFDkzWm3R3vR6T159SCESvQHLoUkv7kqswDkBiW%2Bjqk8rRlO9p20ZsqzcxyJcls4flhzczyBRA8Y'
            'Nu6N6gb%2BylV12CasXcEYA%2F4owOfeWtWHR7YxLfIA%3D%3D'
        )

        self.assertEqual(get_url_signature(self.key, signature_str), expected_output)


class TestVerify(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(sys.prefix, "csob_keys/mips_iplatebnibrana.csob.cz.pub")) as f:
            cls.gateway_pub_key = f.read()

    def test_verify_signature(self):
        signature_str = '20190312144643|0|OK'
        signature = (
            'ktff0QgQsl15PYt2O5rLA0h0ncCUB2F6JPTOzaIPvJP7/pyV2nphurt8/Lr+OykI7TsLr3ElM/S0BEHXxaPs/mtsYkxKswdnCWAfDGczs'
            'cAr1ysd7BWstPwMPV3LATyN3jeHXO+8Z1Ycru9GC9lYKVmrtpl5KVH/N0hP7IUOpx6McbzVGdhhJFpFrJnLQYjZ/94sLvBWi2zzthlkFh'
            '2q4c2eUsVGEKAePFmbnyCL4NPrxdgVzxtVUH80Ywna23ho+9H03JBcV8KkBiD5ABgXCAtQJz3Naa0lZRCiyOLMb8lX/3RWgDGBCr3WIM6'
            '5iiDq00o8tM9VXto6lfczK8a8zQ=='
        )

        self.assertTrue(verify_signature(self.gateway_pub_key, signature_str, signature))

    def test_verify_signature_error(self):
        signature_str = '20190312144643|1|FOOBAR'
        signature = (
            'ktff0QgQsl15PYt2O5rLA0h0ncCUB2F6JPTOzaIPvJP7/pyV2nphurt8/Lr+OykI7TsLr3ElM/S0BEHXxaPs/mtsYkxKswdnCWAfDGczs'
            'cAr1ysd7BWstPwMPV3LATyN3jeHXO+8Z1Ycru9GC9lYKVmrtpl5KVH/N0hP7IUOpx6McbzVGdhhJFpFrJnLQYjZ/94sLvBWi2zzthlkFh'
            '2q4c2eUsVGEKAePFmbnyCL4NPrxdgVzxtVUH80Ywna23ho+9H03JBcV8KkBiD5ABgXCAtQJz3Naa0lZRCiyOLMb8lX/3RWgDGBCr3WIM6'
            '5iiDq00o8tM9VXto6lfczK8a8zQ=='
        )

        self.assertFalse(verify_signature(self.gateway_pub_key, signature_str, signature))
