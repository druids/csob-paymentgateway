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

    1) Payment initiated – this is the initial status after the payment/init method is called. If the initiation is
                           successful, the payer is waiting until he/she is redirected from the e-shop to the payment
                           gateway website. If the transaction may not be initiated, e.g. due to an error in entry data
                           or because the merchant is not authorised to do such operation, the request falls into
                           6) Payment denied status.
    2) Payment in progress – After the payer is redirected to the payment gateway page, the transaction changes its
                             status to the payment in progress status. In the background, many steps take place,
                             ranging from the detection whether the card should be 3D secure verified, and the
                             verification by the issuing bank to the card payment. Such steps are hidden for the
                             merchant, the merchant is interested in the result. The result may be:

                                3) Payment cancelled – the payment was cancelled by the payer on the payment gateway;
                                6) Payment denied – denied by the bank due to the lack of funds, non-confirmation of
                                                    3D secure verification by the payer or for another reason,
                                                    or the process was interrupted, e.g. the payer closed the browser;
                                4) Payment confirmed – the payment was confirmed and it is waiting until the merchant
                                                       adds it to settlement. Successful payments get into this status
                                                       if the automatic inclusion in settlement is inactive.
                                7) Waiting for settlement – the payment was made and automatically put in the queue
                                                            for settlement
    3) Payment cancelled – This status happens when the payer clicks on the Cancel button on the payment gateway page.
                           The payer returns automatically to the e-shop (the payment gateway redirects him/her).
                           In terms of the transaction life cycle, the status is final. If the payer wishes to pay
                           by card for the identical order from the e-shop, the e-shop must generate
                           a new payment request.
    4) Payment confirmed – This status happens after the transaction has been made successfully, if the automatic
                           inclusion in settlement is inactive. As early as the payment initiation step, we choose
                           whether we want to send the transaction for settlement and transfer the money to
                           the merchant’s account after it is confirmed or whether the authorised transaction
                           should wait, e.g. until we get prepare the goods, and the transaction is not put in the
                           queue for settlement until the goods have been shipped.

                           The payment cannot have such status for more than seven days. During this period,
                           the payment is guaranteed by the bank and the funds are blocked on the payer’s card.
                           CAUTION! After the period mentioned above expires, the transaction may not be put
                           on the settlement queue! (The funds on the payer’s card are automatically unblocked
                           by the system and the bank no longer guarantees the payment.)
    5) Payment reversed – Until the confirmed payment is settled, it can be reversed. This means that the cardholder
                          will not be debited, the blocked funds on the card will be released and no fee will be paid.
                          This status is final and it cannot be unreversed. The number of payments reversed
                          by the merchant is monitored by the bank.

                          You can count on the option of payment reversal until the transaction is sent for
                          settlement, i.e. it's possible for transactions in "Payment confirmed" state.
                          For transactions in "Waiting for settlement" state payment reversal is possible till midnight
                          of the given day, after this moment transactions are sent into settlement process. Only refund
                          operation is possible for settled payments.
    6) Payment denied   – This status was already discussed above. There are many reasons for payment denial,
                          they are differentiated in detail in the Operation Return Code. Basically, they can be
                          divided into several groups:
                            * Payment initiation contained erroneous data;
                            * Merchant is not authorised to perform the payment operation;
                            * 3D secure verification was not correctly performed by the payer;
                            * Payer’s bank (card issuer) did not approve card payment;
                            * Payer closed the browser and the transaction expired.
                            * Payment denial by the bank is a specific status. Only the return code indicates
                              for which reason the issuing bank denied the transaction. From the merchant’s point of
                              view, this is an unsuccessful payment and this detail is only for the
                              merchant’s information.

                          If the card payment is unsuccessful, the payer’s card payments are not doomed to failure.
                          The payment gateway offers the payer to pay with another card. The reason is that return
                          to the e-shop and payment failure should not discourage the payers from buying.
                          From the merchant’s point of view, this “transaction for the second time” is all the time
                          in the Payment in progress status, the payment does not change its status until
                          the final success or failure is known.
    7) Waiting for settlement – is a status when transactions are already put in a queue and processed depending
                                on the bank’s settlement rules. Until the transaction is settled, it can be reversed,
                                as described earlier.
    8) Payment settled – is the desired final status for the merchant. Everything was done,
                         the transaction was put in the queue for settlement, settlement was done and the money
                         is on the way. This status if final, but the merchant can choose to cancel the transaction
                         (e.g. the customer cancels the order, or the goods are returned within statutory time-limits),
                         the refund operation may be triggered.
    9) Refund processing – if the merchant requests refund processing, the existing transaction gets into this status
                           and the operation is in progress. Refund processing is approved by the bank on the basis
                           of information provided by the merchant, this status may last for several days.
    10) Payment returned – This phase is reached by the transaction life cycle after refund was approved and after
                           the transaction was made in reverse order to the payer.
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
