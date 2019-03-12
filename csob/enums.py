from enum import Enum, IntEnum


class PayOperation(Enum):
    """
    Type of payment operation.
    """

    PAYMENT = "payment"
    ONE_CLICK_PAYMENT = "oneclickPayment"


class PayMethod(Enum):
    """
    Type of implicit payment method to be offered to the customer.
    """

    CARD = "card"


class Currency(Enum):
    """
    Currency code.
    """

    CZK = "CZK"
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    HUF = "HUF"
    PLN = "PLN"
    HRK = "HRK"
    RON = "RON"
    NOK = "NOK"
    SEK = "SEK"


class HTTPMethod(Enum):
    """
    The return method to e-shop’s URL.
    """

    POST = "POST"
    GET = "GET"


class Language(Enum):
    """
    Preferred language mutation to be displayed on the payment gateway.
    """

    CZ = "CZ"
    EN = "EN"
    DE = "DE"
    FR = "FR"
    HU = "HU"
    IT = "IT"
    JP = "JP"
    PL = "PL"
    PT = "PT"
    RO = "RO"
    RU = "RU"
    SK = "SK"
    ES = "ES"
    TR = "TR"
    VN = "VN"
    HR = "HR"
    SI = "SI"


class PaymentButtonBrand(Enum):
    """
    The payment button brand.
    """
    CSOB = "csob"
    ERA = "era"


class PaymentStatus(IntEnum):
    """
    Payment transactions statuses.

    Payment transactions are done in several steps influenced by the merchant, payer and the payment card status.
    The whole life cycle, starting from the payment initiation to the payment completion, including any further
    statuses initiated by the merchant, are shown in the next diagram. We will describe them in detail:

    1) Payment initiated – this is the initial status after the payment/init method is called.
    2) Payment in progress – The payer has been redirected to the gateway page.
    3) Payment cancelled – This status happens when the payer clicks on the Cancel button on the payment gateway page.
    4) Payment confirmed – This status happens after the transaction has been made successfully.
    5) Payment reversed – Until the confirmed payment is settled, it can be reversed.
    6) Payment denied   – The payment has been denied see Operation Return Code for detail.
    7) Waiting for settlement – is a status when transactions are already put in a queue and might be being processed.
    8) Payment settled – is the desired final status for the merchant. Everything was done, money is on the way.
    9) Refund processing – Payment refund operation in progress.
    10) Payment returned – Payment has been refunded and money has been sent to the payer.

    See Also:
        https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#transaction-life-cycle
    """

    PAYMENT_INIT = 1
    PAYMENT_IN_PROGRESS = 2
    PAYMENT_CANCELED = 3
    PAYMENT_CONFIRMED = 4
    PAYMENT_REVERSED = 5
    PAYMENT_DENIED = 6
    PAYMENT_WAITING_FOR_SETTLEMENT = 7
    PAYMENT_SETTLED = 8
    PAYMENT_REFUND_PROCESSING = 9
    PAYMENT_RETURNED = 10


class ResultCode(IntEnum):
    """
    Possible result codes from API.

    See Also:
        https://github.com/csob/paymentgateway/wiki/eAPI-v1.7-EN#return-code-register-
    """
    INTERNAL_ERROR = 900
    CUSTOMER_HAVE_CARDS = 820
    CUSTOMER_NO_CARDS = 810
    CUSTOMER_NOT_FOUND = 800
    EET_REJECTED = 500
    OPERATION_NOT_ALLOWED = 180
    PAYMENT_INVALID_STATE = 150
    PAYMENT_NOT_FOUND = 140
    SESSION_EXPIRED = 130
    MERCHANT_BLOCKED = 120
    INVALID_PARAMETER = 110
    MISSING_PARAMETER = 100
    OK = 0
