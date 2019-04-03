from typing import Optional, TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from csob.api import APIResponse


class CSOBBaseException(Exception):
    response: Optional[requests.Response]

    def __init__(self, response: Optional[requests.Response] = None) -> None:
        self.response = response


class GatewaySignatureInvalid(CSOBBaseException):
    pass


class ServiceResponseException(CSOBBaseException):
    http_code: int


class BadRequestResponseException(ServiceResponseException):
    """
    The service responded with 400 - Bad Request.

    The request cannot be handled. The request has bad syntax.
    """

    http_code = 400


class ForbiddenResponseException(ServiceResponseException):
    """
    The service responded with 403 - Forbidden.

    Access denied.
    """

    http_code = 403


class NotFoundResponseException(ServiceResponseException):
    """
    The service responded with 404 - Not Found.

    The source was not found.
    """

    http_code = 404


class MethodNotAllowedResponseException(ServiceResponseException):
    """
    The service responded with 405 - Method Not Allowed.

    The requested method is not supported.
    """

    http_code = 405


class TooManyRequestsResponseException(ServiceResponseException):
    """
    The service responded with 429 - Too Many Requests.


    The user has sent too many requests.
    """

    http_code = 429


class ServiceUnavailableResponseException(ServiceResponseException):
    """
    The service responded with 503 - Service Unavailable.

    The service is temporarily unavailable.
    """

    http_code = 503


HTTP_ERROR_CSOB_EXCEPTIONS = {
    400: BadRequestResponseException,
    403: ForbiddenResponseException,
    404: NotFoundResponseException,
    405: MethodNotAllowedResponseException,
    429: TooManyRequestsResponseException,
    503: ServiceUnavailableResponseException,
}


class ServiceResultCodeException(CSOBBaseException):
    code: int
    message: str
    api_response: Optional["APIResponse"]

    def __init__(self, response=None, message=None, api_response=None):
        self.message = message
        self.api_response = api_response
        super().__init__(response)


class MissingParameterResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 100 - Missing Parameter.

    Missing mandatory parameter

    Format: Missing parameter {name}
    """

    code = 100


class InvalidParameterResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 110 - Invalid parameter.

    Bad format of parameter

    Format: Invalid parameter {name}
    """

    code = 110


class MerchantBlockedResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 120 - Merchant blocked.

    Merchant is not authorised to accept payments.

    Format: Merchant blocked
    """

    code = 120


class SessionExpiredResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 130 - Session expired.

    Request validity expired

    Format: Session expired
    """

    code = 130


class PaymentNotFoundResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 140 - Payment not found.

    Payment not found

    Format: Payment not found
    """

    code = 140


class PaymentInvalidStateResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 150 - Payment not in valid state.

    Bad payment state, operation cannot be performed

    Format: Payment not in valid state
    """

    code = 150


class OperationNotAllowedResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 180 - Operation not allowed.

    Operation not allowed

    Format: Operation not allowed
    """

    code = 180


class EETRejectedResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 500 - EET Rejected.

    EET report was rejected by FS

    Format: EET Rejected
    """

    code = 500


class CustomerNotFoundResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 800 - Customer not found.

    Customer identified by customerId not found

    Format: Customer not found
    """

    code = 800


class InternalErrorResultCodeException(ServiceResultCodeException):
    """
    The service responded with Result code 900 - Internal error.

    Internal error in request processing

    Format: Internal error
    """
    code = 900


SERVICE_RESULT_CODE_EXCEPTION_DICT = {
    900: InternalErrorResultCodeException,
    800: CustomerNotFoundResultCodeException,
    500: EETRejectedResultCodeException,
    180: OperationNotAllowedResultCodeException,
    150: PaymentInvalidStateResultCodeException,
    140: PaymentNotFoundResultCodeException,
    130: SessionExpiredResultCodeException,
    120: MerchantBlockedResultCodeException,
    110: InvalidParameterResultCodeException,
    100: MissingParameterResultCodeException,
}
