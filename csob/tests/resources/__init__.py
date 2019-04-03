import os
import sys

PRIVATE_KEY_PATH = os.path.join(sys.prefix, 'csob_keys/rsa_test_A3746UdxZO.key')
GATEWAY_KEY_PATH = os.path.join(sys.prefix, 'csob_keys/mips_platebnibrana.csob.cz.pub')


def get_private_key():
    with open(PRIVATE_KEY_PATH, 'r') as f:
        return f.read()


def get_gateway_key():
    with open(GATEWAY_KEY_PATH, 'r') as f:
        return f.read()
