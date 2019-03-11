from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from csob_paymentgateway.enums import (
    Currency, HTTPMethod, Language, PaymentButtonBrand, PayMethod, PayOperation, ResultCode
)
from csob_paymentgateway.payment import Item, Payment


AmountHundredths = Union[Decimal, int]


class APIResponse:
    response_json: dict
    date_time: datetime
    signature: str
    result_code: ResultCode

    def get_payment_data(self) -> Payment:
        """
        From response_json get Payment object.

        Returns:
            Payment
        """
        raise NotImplementedError()

    def is_okay(self) -> bool:
        """
        Check if result code is OK or 8*0.

        Returns:
            bool
        """
        raise NotImplementedError()


class API:
    """
    The base class which holds config and provides API calls.

    Attributes:
    """
    merchant_id: str
    raise_exceptions: bool

    def __init__(self, merchant_id: str, private_key_path: str, gateway_public_key_path: Optional[str] = None,
                 private_key_password: Optional[str] = None, api_url: str = "https://api.platebnibrana.csob.cz",
                 raise_exceptions: bool = False):
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
            If cart specified at least 1 item (e.g. “Your purchase”) and at most 2 items must be in the cart
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

        Payment initiation payment/init As soon as the final phase of a purchase is initiated in the e-shop, the payer
        proceeds to payment and chooses to pay by a card, the e-shop initiates a payment on the payment gateway.
        Besides standard information, such as merchant identification, amount and order reference number, the e-shop
        can forward purchase details, incl. cart items, to the payment gateway to make the payment process clearer and
        more transparent and to increase the customer confidence in the correct process of operations in the e-shop and
        payment gateway.

        Order reference number is assigned by the merchant’s e-shop. Finally, the order reference number will appear on
        the bank statement of transactions. The number is thus used in the merchant’s system (accounting) for pairing
        of payments with orders. Therefore, the symbol is obligatory (numeric value with maximum 10 digits).
        Order reference number is displayed as Variable symbol in POSMerchant application.

        After payment initiation, the payment gateway assigns payID, a unique payment ID, to each transaction.
        This identifier returns in the response to payment/init and it accompanies the payment transaction in all
        its statuses.

        Order number, which the merchant forwards to the payment gateway upon the payment initiation, must be unique
        in the merchant’s e-shop. If the merchant initiates two transactions with the identical order number on the
        payment gateway, the transactions will have different payId’s, but they will appear as two payments with the
        identical variable symbol on the bank statement.

        If the customer has logged in to the e-shop and his/her identity is known, it is possible to forward the
        customer’s unique identifier. This will enable the customer to have the gateway remember his/her payment
        card securely on the gateway and to use it again without having to enter the card’s long number.

        Notes:
            Please note: when payOperation is set to oneclickPayment, the customerId parameter is ignored.
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
                         payment gateway. Therefore, a brief description is sent to the bank. Maximum length is
                         255 characters
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

    def get_payment_process_url(self, pay_id: str) -> str:
        """
        Get the url to redirect the user to after payment initialization.

        See Also:
            https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#get--httpsapiplatebnibranacsobczapiv17paymentprocess-  # noqa

        Args:
            pay_id: Unique payment ID (assigned by the payment gateway in the init operation)

        Returns:
            url
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

        Return values are identical with the definition described with the payment/init operation supplemented by the
        merchantData parameter. They are forwarded to the e-shop’s return address
        (returnUrl parameter obtained in the payment/init) via the payer’s browser using the GET
        (returnMethod parameter).

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

        Return values are identical with the definition described with the payment/init operation supplemented by the
        merchantData parameter. They are forwarded to the e-shop’s return address
        (returnUrl parameter obtained in the payment/init) via the payer’s browser using the POST
        (returnMethod parameter).

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

        The operation reverses (i.e. cancels before the transaction is sent to the end-of-day procedure) an already
        authorised transaction. If such function is called for a transaction which has already left for the
        EoD procedure, an error returns. In this case a request for refund must be entered to reverse the transaction.

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

        By calling the operation, a request for refund to the payer is made.
        This is applied to transactions already added to settlement. This method also supports partial refunds
        (by setting the amount parameter). This partial refund can be called multiple times,
        but the sum of refunds can not exceed the original transaction amount.

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

        An additional operation which is used to verify the correctness of the request signature, and to check the
        response signature during the application development.

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
