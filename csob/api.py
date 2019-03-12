from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from csob.enums import (
    Currency, HTTPMethod, Language, PaymentButtonBrand, PayMethod, PayOperation, ResultCode
)
from csob.payment import Item


AmountHundredths = Union[Decimal, int]


class APIResponse:
    response_json: dict
    date_time: datetime
    signature: str
    result_code: ResultCode

    def is_okay(self) -> bool:
        """
        Check if result code is OK or 8*0.

        Returns:
            bool
        """
        raise NotImplementedError()


class APIClient:
    """
    The base class which holds config and provides API calls.

    Attributes:
    """
    merchant_id: str
    raise_exceptions: bool

    def __init__(self, merchant_id: str, private_key_path: str, gateway_public_key_path: Optional[str] = None,
                 private_key_password: Optional[str] = None, api_url: str = "https://api.platebnibrana.csob.cz",
                 raise_exceptions: bool = False) -> None:
        """
        Load private and public key.

        Args:
            merchant_id: Merchant’s ID assigned by the payment gateway
            private_key_path: Path to Merchant’s private key
            gateway_public_key_path: Path to Payment Gateway's public key
            private_key_password: Optional password to Merchant’s private key
            api_url: The API's url
            raise_exceptions: Whether should functions return APIResponse with errors or raise exceptions.

        Warnings:
            If cart specified is specified it has to have at least 1 item (e.g. “Your purchase”) and at most 2 items.
            (e.g. “Your purchase” and “Shipping & Handling”). The limitation is given by the graphical design.
        """
        raise NotImplementedError()

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
                they must be BASE64 encoded. Maximum length for encoding is 255 characters
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
        raise NotImplementedError()

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
        raise NotImplementedError()

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

    def parse_payment_return_url_get(self, url: str) -> APIResponse:
        """
        Parse the incoming redirect from payment gate.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#return-url---return-to-do-e-shop-

        Notes:
            e-shop must support response processing of both GET and/or POST http methods
            (payment gateway will execute redirect according to returnMethod parameter, but for specific actions
            -- e.g. cancel payment by user -- GET redirect is always performed).

        Args:
            url: The url to which the user has been redirected from the payment gateway.

        Returns:
            APIResponse - Return values are identical with the definition contained in the payment/init operation.
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

    def payment_refund(self, pay_id: str, amount: Optional[AmountHundredths]) -> APIResponse:
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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()
