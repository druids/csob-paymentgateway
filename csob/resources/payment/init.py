import json
from typing import Optional, List

from csob.api_response import APIResponse

from csob.resources.payment import PaymentCSOBResource


class PaymentInitResource(PaymentCSOBResource):
    url = 'payment/init'
    request_signature = (
        'merchantId', 'orderNo', 'dttm', 'payOperation', 'payMethod', 'totalAmount', 'currency', 'closePayment',
        'returnUrl', 'returnMethod', 'cart', 'description', 'merchantData', 'customerId', 'language', 'ttlSec',
        'logoVersion', 'colorSchemeVersion')
    optional_request_signature = ('merchantData', 'customerId', 'ttlSec', 'logoVersion', 'colorSchemeVersion')

    def post(self, order_number: str, pay_operation: str, pay_method: str, total_amount: int, currency: str,
             close_payment: bool, return_url: str, return_method: str, description: str, language: str,
             merchant_data: Optional[str], customer_id: Optional[str], cart: Optional[List[dict]] = None,
             ttl_sec: Optional[int] = None, logo_version: Optional[int] = None,
             color_scheme_version: Optional[int] = None) -> APIResponse:
        local_json = self.get_base_json()

        if len(order_number) > 10:
            raise ValueError('orderNo is too long.')
        local_json['orderNo'] = order_number

        if pay_operation not in {'payment', 'oneclickPayment'}:
            raise ValueError('payOperation invalid value')
        local_json['payOperation'] = pay_operation

        if pay_method != 'card':
            raise ValueError('payMethod invalid value')
        local_json['payMethod'] = pay_method

        if not isinstance(total_amount, int):
            raise ValueError('totalAmount invalid value')
        local_json['totalAmount'] = total_amount

        if currency not in {'CZK', 'EUR', 'USD', 'GBP', 'HUF', 'PLN', 'HRK', 'RON', 'NOK', 'SEK'}:
            raise ValueError('curreny invalid value')
        local_json['currency'] = currency

        if not isinstance(close_payment, bool):
            raise ValueError('closePayment invalid value')
        local_json['closePayment'] = close_payment

        if len(return_url) > 300:
            raise ValueError('returnUrl is too long')
        local_json['returnUrl'] = return_url

        if return_method not in {'POST', 'GET'}:
            raise ValueError('returnMethod invalid value')
        local_json['returnMethod'] = return_method

        if len(description) > 255:
            raise ValueError('description is too long')
        local_json['description'] = description

        if language not in {'CZ', 'EN', 'DE', 'FR', 'HU', 'IT', 'JP', 'PL', 'PT', 'RO', 'RU', 'SK', 'ES', 'TR', 'VN',
                            'HR', 'SI'}:
            raise ValueError('language is invalid')
        local_json['language'] = language

        if merchant_data is not None:
            if len(merchant_data) > 255:
                raise ValueError('merchantData is too long')
            local_json['merchantData'] = merchant_data

        if customer_id is not None:
            if len(customer_id) > 50:
                raise ValueError('customerId is too long')
            local_json['customerId'] = customer_id

        if cart is None:
            cart = [{
                'name': 'Your purchase',
                'quantity': 1,
                'amount': total_amount,
            }]
        local_json['cart'] = cart

        if ttl_sec is not None:
            if isinstance(ttl_sec, int) and 300 <= ttl_sec <= 1800:
                local_json['ttlSec'] = ttl_sec
            else:
                raise ValueError('ttlSec not in range')

        if logo_version is not None:
            if isinstance(logo_version, int):
                local_json['logoVersion'] = logo_version
            else:
                raise ValueError('logoVersion is not a number.')

        if color_scheme_version is not None:
            if isinstance(color_scheme_version, int):
                local_json['colorSchemeVersion'] = color_scheme_version
            else:
                raise ValueError('colorSchemeVersion is not a number.')

        return self._sign_and_post(local_json)
