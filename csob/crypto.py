from base64 import b64decode, b64encode
from urllib import parse

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def get_signature(key: str, signature_str: str) -> str:
    """
    Sign a signature string with SHA-1 RSA.

    Args:
        key: private key in string representation
        signature_str: String to be signed

    Returns:

    """
    signer = PKCS1_v1_5.new(RSA.importKey(key))

    signature = signer.sign(SHA.new(signature_str.encode('utf-8')))

    return b64encode(signature).decode('utf-8')


def get_url_signature(key, signature_str):
    """
    Urlize signature from `csob.crypto.get_signature`.

    Args:
        key: private key in string representation
        signature_str: String to be signed

    Returns:
        urlize signature
    """
    return parse.quote_plus(get_signature(key, signature_str))


def verify_signature(public_key: str, signature_str: str, signature: str) -> bool:
    """
    Verify incoming signature that it is correct.

    Args:
        public_key: Public key to use
        signature_str: String that was signed
        signature: The provided signature

    Returns:
        bool
    """
    verifier = PKCS1_v1_5.new(RSA.importKey(public_key))

    return verifier.verify(SHA.new(signature_str.encode('utf-8')), b64decode(signature))
