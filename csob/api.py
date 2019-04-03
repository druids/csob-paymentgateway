import os
import sys
from base64 import b64encode
from decimal import Decimal
from typing import List, Optional, Union, Dict

import requests
import import_string
from cached_property import cached_property

from csob.api_response import APIResponse
from csob.enums import (
    Currency, HTTPMethod, Language, PaymentButtonBrand, PayMethod, PayOperation)
from csob.payment import Item
from csob.resources.echo import EchoResource
from csob.resources.payment.close import PaymentCloseResource
from csob.resources.customer.info import CustomerInfoResource
from csob.resources.payment.init import PaymentInitResource
from csob.resources.payment.process import PaymentProcessResource
from csob.resources.payment.refund import PaymentRefundResource
from csob.resources.payment.reverse import PaymentReverseResource
from csob.resources.payment.status import PaymentStatusResource

AmountHundredths = Union[Decimal, int]


class APIClient:
    """
    The base class which holds config and provides API calls.

    Attributes:
    """
    merchant_id: str
    private_key_path: str
    gateway_public_key_path: str
    _gateway_public_key: Optional[str] = None
    api_url: str
    session: requests.Session
    raise_exceptions: bool

    def __init__(self, merchant_id: str, private_key_path: str, gateway_public_key_path: Optional[str] = None,
                 api_url: str = 'https://api.platebnibrana.csob.cz/api/v1.7/',
                 session_generator_str: Optional[str] = None, raise_exceptions: bool = True) -> None:
        """
        Load private and public key.

        Args:
            merchant_id: Merchant’s ID assigned by the payment gateway
            private_key_path: Path to Merchant’s private key
            gateway_public_key_path: Path to Payment Gateway's public key
            api_url: The API's url
            session_generator_str: Python package path to the Session generator
            raise_exceptions: Whether should functions return APIResponse with errors or raise exceptions.

        Warnings:
            If cart specified is specified it has to have at least 1 item (e.g. “Your purchase”) and at most 2 items.
            (e.g. “Your purchase” and “Shipping & Handling”). The limitation is given by the graphical design.
        """
        self.raise_exceptions = raise_exceptions
        self.session = import_string(session_generator_str) if session_generator_str is not None else requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.api_url = api_url
        self.gateway_public_key_path = (
            gateway_public_key_path or os.path.join(sys.prefix, 'csob_keys/mips_platebnibrana.csob.cz.pub'))
        self.private_key_path = private_key_path
        self.merchant_id = merchant_id

    def payment_init(self, order_number: str, total_amount: AmountHundredths,
                     close_payment: bool, return_url: str, description: str,
                     cart: Optional[List[Item]] = None,
                     return_method: HTTPMethod = HTTPMethod.POST,
                     currency: Currency = Currency.CZK,
                     pay_operation: PayOperation = PayOperation.PAYMENT,
                     pay_method: PayMethod = PayMethod.CARD,
                     merchant_data: Optional[str] = None,
                     customer_id: Optional[str] = None,
                     language: Language = Language.CZ,
                     ttl_sec: Optional[int] = None,
                     logo_version: Optional[int] = None,
                     color_scheme_version: Optional[int] = None) -> APIResponse:
        """
        Initialize new payment.

        Notes:
            Please note: when payOperation is set to oneclick Payment, the customerId parameter is ignored.
            Your customer will always need to enter the card details, it is not possible to convert a previously
            remembered card on the gateway to a template for oneclick payments.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#-post-httpsapiplatebnibranacsobczapiv17paymentinit-

        Args:
            order_number: Reference number of the order used to match payments. The number will also be indicated on
                the bank statement. A numeric value, 10 digits max.
            total_amount: Total amount in hundredths of the basic currency. This value will appear on the payment
                gateway as the total amount to be paid. (Decimals are automatically converted.)
            close_payment: It indicates whether the payment should automatically be put in the queue for settlement
                and paid.
            return_url: URL to which the customer will be redirected after the payment has been completed. Maximum
                length is 300 characters.
            description: Brief description of the purchase for 3DS page: In case of customer verification on the
                issuing bank’s side, the detail of the cart cannot be displayed as it is possible on the
                payment gateway. Therefore, a brief description is sent to the bank. Maximum length is 255 characters
            cart: A list of items to be displayed on the payment gateway.
            return_method: The return method to e-shop’s URL.
            currency: Currency code.
            pay_operation: Type of payment operation.
            pay_method: Type of implicit payment method to be offered to the customer.
            merchant_data: Any additional data which are returned in the redirect from the payment gateway to the
                merchant’s page. Such data may be used to keep continuity of the process in the e-shop,
                they will be BASE64 encoded. Maximum length for encoding is 255 characters.
            customer_id: Unique customer ID assigned by the e-shop. Maximum length is 50 characters. It is used if
                the customer’s card is remembered on the gateway and will be used to simplify next payments
            language: Preferred language mutation to be displayed on the payment gateway.
            ttl_sec: Transaction lifetime in seconds, min. 300, max. 1800 (5-30 min). Use in case you need to
                limit the time the customer can
            logo_version: Version of the merchant logo. Approved version must be provided
                (if not, available approved version will be used). Should no approved logo be available
                for merchant, default placeholder will be shown.
            color_scheme_version: Version of the merchant colour scheme. Approved version must be provided
                (if not, available approved version will be used). Should no approved logo
                be available for merchant, default placeholder will be shown.

        Returns:
            APIResponse
        """
        if isinstance(total_amount, Decimal):
            total_amount = int(total_amount * 100)

        return PaymentInitResource(**self.resource_kwargs).post(
            order_number=order_number, pay_operation=pay_operation.value,
            pay_method=pay_method.value, total_amount=total_amount, currency=currency.value,
            close_payment=close_payment, return_url=return_url, return_method=return_method.value,
            description=description, language=language.value, merchant_data=b64encode(merchant_data),
            customer_id=customer_id, cart=([i.dict for i in cart] if cart is not None else None),
            ttl_sec=ttl_sec, logo_version=logo_version, color_scheme_version=color_scheme_version
        )

    def get_payment_process_url(self, pay_id: str) -> APIResponse:
        """
        Get the url to redirect the user to after payment initialization.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#get--httpsapiplatebnibranacsobczapiv17paymentprocess-  # noqa

        Args:
            pay_id: Unique payment ID (assigned by the payment gateway in the init operation)

        Returns:
            APIResponse
        """
        return PaymentProcessResource(**self.resource_kwargs).get(pay_id)

    def get_payment_button_params(self, pay_id: str, brand: PaymentButtonBrand) -> APIResponse:
        """
        Returns parameters used by the merchant to redirect the customer to CSOB / ERA electronic banking.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#post-httpsapiplatebnibranacsobczapiv17paymentbutton-  # noqa

        Args:
            pay_id: Unique payment ID (assigned by the payment gateway in the init operation)
            brand: Payment button brand selected by the customer.

        Returns:
            APIResponse
        """
        raise NotImplementedError()

    def parse_payment_return_url_get(self, get_dict: dict) -> APIResponse:
        """
        Parse the incoming redirect from payment gate.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#return-url---return-to-do-e-shop-

        Notes:
            e-shop must support response processing of both GET and/or POST http methods
            (payment gateway will execute redirect according to returnMethod parameter, but for specific actions
            -- e.g. cancel payment by user -- GET redirect is always performed).

        Args:
            get_dict: The get parameters received

        Returns:
            APIResponse - Return values are identical with the definition contained in the payment/init operation.
        """
        return PaymentProcessResource(**self.resource_kwargs).parse_response_dict(get_dict)

    def parse_payment_return_url_post(self, post_data: dict) -> APIResponse:
        """
        Parse the incoming redirect from payment gate.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#return-url---return-to-do-e-shop-

        Notes:
            e-shop must support response processing of both GET and/or POST http methods
            (payment gateway will execute redirect according to returnMethod parameter, but for specific actions
            -- e.g. cancel payment by user -- GET redirect is always performed).

        Args:
            post_data: The POST data received from redirect.

        Returns:
            APIResponse - Return values are identical with the definition contained in the payment/init operation.
        """
        return PaymentProcessResource(**self.resource_kwargs).parse_response_dict(post_data)

    def payment_status(self, pay_id: str) -> APIResponse:
        """
        Get status of a payment.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#get-httpsapiplatebnibranacsobczapiv17paymentstatus-

        Args:
            pay_id: Unique payment ID (assigned by the payment gateway in the init operation)

        Returns:
            APIResponse - Return values are identical with the definition contained in the payment/init operation.
        """
        return PaymentStatusResource(**self.resource_kwargs).get(pay_id)

    def payment_reverse(self, pay_id: str) -> APIResponse:
        """
        Reverse already authorised transaction.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#put-httpsapiplatebnibranacsobczapiv17paymentreverse-  # noqa

        Args:
            pay_id: Unique payment ID (assigned by the payment gateway in the init operation)

        Returns:
            APIResponse - Return values are identical with the definition contained in the payment/init operation.
        """
        return PaymentReverseResource(**self.resource_kwargs).put(pay_id)

    def payment_close(self, pay_id: str, total_amount: Optional[AmountHundredths]) -> APIResponse:
        """
        The operation will add the transaction to settlement.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#puthttpsapiplatebnibranacsobczapiv17paymentclose-

        Args:
            pay_id: Unique payment ID (assigned by the payment gateway in the init operation)
            total_amount: Total amount in hundredths of the basic currency. Value must be positive and
                less or equal than original amount (see totalAmount parameter in payment/init operation)
                (Decimals are automatically converted.)

        Returns:
            APIResponse - Return values are identical with the definition contained in the payment/init operation.
        """
        if isinstance(total_amount, Decimal):
            total_amount = int(total_amount * 100)

        return PaymentCloseResource(**self.resource_kwargs).put(pay_id, total_amount)

    def payment_refund(self, pay_id: str, amount: Optional[AmountHundredths] = None) -> APIResponse:
        """
        Refund whole payment or it's part.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#puthttpsapiplatebnibranacsobczapiv17paymentrefund-

        Notes:
            This operation is processed asynchronously on payment gateway side, response parameter paymentStatus
            contains current payment status (which will be Settled payment), monitoring of payment changes is
            available via payment/status operation.

        Args:
            pay_id: Unique payment ID (assigned by the payment gateway in the init operation)
            amount: Requested refund amount for the partial refund in hundredths of the original currency.
                (Decimals are automatically converted.)

        Returns:
            APIResponse - Return values are identical with the definition contained in the payment/init operation.
        """
        if isinstance(amount, Decimal):
            amount = int(amount * 100)

        return PaymentRefundResource(**self.resource_kwargs).put(pay_id, amount)

    def echo(self, method: HTTPMethod = HTTPMethod.GET) -> APIResponse:
        """
        Test if API is working and provided merchant_id and private_key are valid.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#getpost-httpsapiplatebnibranacsobczapiv17echo-

        Args:
            method: The operation may be called using the POST method (parameters are sent in the request body in the
                JSON format) or using the GET method – the request contains items directly in the URL.

        Returns:
            APIResponse
        """
        resource = EchoResource(**self.resource_kwargs)
        if method == HTTPMethod.GET:
            return resource.get()
        elif method == HTTPMethod.POST:
            return resource.post()
        else:
            raise ValueError('Invalid method for `echo`.')

    def customer_info(self, customer_id: str) -> APIResponse:
        """
        List information about customers with remembered cards.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#gethttpsapiplatebnibranacsobczapiv17customerinfo-

        Args:
            customer_id: Customer’s ID assigned in the e-shop, maximum length 50 characters.

        Returns:
            APIResponse
        """
        return CustomerInfoResource(**self.resource_kwargs).get(customer_id)

    @cached_property
    def _private_key(self) -> str:
        """
        Get text representation of private key.

        Returns:
            str
        """
        with open(self.private_key_path, 'r') as f:
            return f.read()

    @cached_property
    def gateway_public_key(self) -> str:
        """
        Get text representation of private key.

        Returns:
            str
        """
        if self._gateway_public_key is not None:
            return self._gateway_public_key

        with open(self.gateway_public_key_path, 'r') as f:
            self._gateway_public_key = f.read()

        return self._gateway_public_key

    @cached_property
    def resource_kwargs(self) -> Dict:
        return {
            'base_url': self.api_url,
            'merchant_id': self.merchant_id,
            'gateway_key': self.gateway_public_key,
            'private_key': self._private_key,
            'session': self.session,
            'raise_exception': self.raise_exceptions,
        }
