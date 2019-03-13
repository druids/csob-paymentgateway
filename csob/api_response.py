from datetime import datetime
from typing import Optional

from requests import Response

from csob.enums import ResultCode
from csob.exceptions import SERVICE_RESULT_CODE_EXCEPTION_DICT


class APIResponse:
    api_response: Response
    is_verified: Optional[bool]

    def __init__(self, api_response: Response, is_verified: Optional[bool], raise_exception=False):
        self.api_response = api_response
        self.is_verified = is_verified

        if self.is_verified:
            if raise_exception and self.is_okay is False:
                raise SERVICE_RESULT_CODE_EXCEPTION_DICT[self.result_code]

    @property
    def response_json(self) -> Optional[dict]:
        if self.http_status_code == 200:
            return self.api_response.json()

    @property
    def http_status_code(self) -> int:
        return self.api_response.status_code

    @property
    def result_code(self) -> Optional[ResultCode]:
        if self.response_json is not None:
            return self.response_json['resultCode']

    @property
    def result_message(self) -> Optional[str]:
        if self.response_json is not None:
            return self.response_json['resultMessage']

    @property
    def is_okay(self) -> bool:
        """
        Check if result code is OK or 810 or 820.

        Returns:
            bool
        """
        if self.api_response.status_code == 200:
            return self.result_code in [0, 810, 820]
        return False
