from typing import Optional

from cached_property import cached_property
from requests import Response

from csob.enums import ResultCode, PaymentStatus
from csob.exceptions import SERVICE_RESULT_CODE_EXCEPTION_DICT


class APIResponse:
    api_response: Optional[Response] = None
    is_verified: Optional[bool] = None
    _parsed_data: Optional[dict] = None

    def __init__(self, api_response: Optional[Response] = None, parsed_data: Optional[dict] = None,
                 is_verified: Optional[bool] = None, raise_exception=False):
        self._parsed_data = parsed_data
        self.api_response = api_response
        if parsed_data is None and api_response is None:
            raise ValueError('You have to specify at least `api_response`')
        self.is_verified = is_verified

        if self.is_verified:
            if raise_exception and self.is_okay is False:
                raise SERVICE_RESULT_CODE_EXCEPTION_DICT[self.result_code]

    @cached_property
    def response_json(self) -> Optional[dict]:
        if self.api_response is not None:
            if self.http_status_code == 200:
                return self.api_response.json()
        else:
            return self._parsed_data

    @cached_property
    def http_status_code(self) -> Optional[int]:
        if self.api_response is not None:
            return self.api_response.status_code
        return None

    @cached_property
    def result_code(self) -> Optional[ResultCode]:
        if self.response_json is not None:
            return self.response_json['resultCode']
        return None

    @cached_property
    def result_message(self) -> Optional[str]:
        if self.response_json is not None:
            return self.response_json['resultMessage']
        return None

    @cached_property
    def is_okay(self) -> bool:
        """
        Check if result code is OK or 810 or 820.

        Returns:
            bool
        """
        if getattr(self.api_response, "status_code", 200) != 200:
            return False

        return self.result_code in [0, 810, 820]

    @cached_property
    def payment_status(self) -> Optional[PaymentStatus]:
        if self.response_json is not None:
            if 'paymentStatus' in self.response_json.keys():
                return PaymentStatus(self.response_json['paymentStatus'])
        return None

    @cached_property
    def auth_code(self) -> Optional[str]:
        if self.response_json is not None:
            if 'authCode' in self.response_json.keys():
                return self.response_json['authCode']
        return None
