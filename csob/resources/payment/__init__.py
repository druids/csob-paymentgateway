from csob.resources import CSOBResource


class PaymentCSOBResource(CSOBResource):
    """
    This class holds common return request signature.
    """
    response_signature = ('payId', 'dttm', 'resultCode', 'resultMessage', 'paymentStatus', 'authCode')
    optional_response_signature = ('paymentStatus', 'authCode')
