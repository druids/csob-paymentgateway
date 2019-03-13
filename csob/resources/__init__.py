from typing import Iterable, Tuple, Dict, Optional
from urllib.parse import urljoin

import requests

from csob.api_response import APIResponse
from csob.crypto import get_signature, get_url_signature, verify_signature
from csob.exceptions import HTTP_ERROR_CSOB_EXCEPTIONS, GatewaySignatureInvalid
from csob.utils import get_dttm


class CSOBResource:
    url: str

    request_signature: Iterable[str]
    optional_request_signature: Tuple[str] = tuple()
    response_signature: Iterable[str]
    optional_response_signature: Tuple[str] = tuple()

    _base_url: str
    _gateway_key: str
    merchant_id: str
    session: requests.Session
    raise_exception = True

    def __init__(self, base_url: str, merchant_id: str, gateway_key: str,
                 session: requests.Session = requests.Session(),
                 raise_exception: bool = True):
        self._gateway_key = gateway_key
        self.raise_exception = raise_exception
        self.merchant_id = merchant_id
        self._base_url = base_url
        self.session = session

    def get_base_json(self) -> dict:
        return {
            'merchantId': self.merchant_id,
            'dttm': get_dttm(),
        }

    def get_url(self):
        return urljoin(self._base_url, self.url)

    def _construct_signature_str(self, json: Dict) -> str:
        """
        From json constructs signature str.

        Args:
            json: JSON from which to get the signature str.

        Returns:
            Signature str
        """
        signature_list = []
        for i in [i for i in self.request_signature if (i not in self.optional_request_signature or i in json.keys())]:
            if type(json[i]) == list:  # Cart list of dicts
                for j in json[i]:
                    signature_list.extend([str(k) for k in j.values()])
            elif json[i] is True:
                signature_list.append('true')
            elif json[i] is False:
                signature_list.append('false')
            else:
                signature_list.append(str(json[i]))
        print(signature_list)

        return "|".join(signature_list)

    def _construct_verify_signature_str(self, json: Dict) -> str:
        """
        From response json constructs signature str.

        Args:
            json: JSON from which to get the signature str.

        Returns:
            Signature str
        """
        return "|".join([str(json[i]) for i in self.response_signature if
                         (i not in self.optional_response_signature or i in json.keys())])

    def get_signature(self, key: str, json: Dict) -> str:
        """
        Construct signature str and calls `csob.crypto.get_signature`.

        Args:
            key: private key in string representation
            json: JSON to be sent from which the signature str is built

        Returns:
            Signature
        """
        return get_signature(key, self._construct_signature_str(json))

    def get_url_signature(self, key: str, json: Dict) -> str:
        """
        Construct signature str and calls `csob.crypto.get_signature`.

        Args:
            key: private key in string representation
            json: JSON to be sent from which the signature str is built

        Returns:
            Signature
        """
        return get_url_signature(key, self._construct_signature_str(json))

    def verify_signature(self, key: str, json: Dict) -> bool:
        """
        Construct signature str for response and calls `csob.crypto.verify_signature`

        Args:
            key: The public gateway key
            json: The JSON to be verified
            signature: The signature to be verified.

        Returns:
            bool
        """
        return verify_signature(key, self._construct_verify_signature_str(json), json['signature'])

    def parse_response(self, response: requests.Response) -> APIResponse:
        """
        Converts `requests.Response` into `APIResponse`

        Args:
            response: Response from the Gateway

        Returns:
            APIResponse

        Raises:
            BadRequestResponseException
            ForbiddenResponseException
            NotFoundResponseException
            MethodNotAllowedResponseException
            TooManyRequestsResponseException
            ServiceUnavailableResponseException
            InternalErrorResultCodeException
            CustomerNotFoundResultCodeException
            EETRejectedResultCodeException
            OperationNotAllowedResultCodeException
            PaymentInvalidStateResultCodeException
            PaymentNotFoundResultCodeException
            SessionExpiredResultCodeException
            MerchantBlockedResultCodeException
            InvalidParameterResultCodeException
            MissingParameterResultCodeException
        """
        if response.status_code != 200:
            if self.raise_exception:
                if response.status_code in HTTP_ERROR_CSOB_EXCEPTIONS.keys():
                    raise HTTP_ERROR_CSOB_EXCEPTIONS[response.status_code](response)
                response.raise_for_status()
            else:
                return APIResponse(response, is_verified=None)

        is_verified = self.verify_signature(self._gateway_key, response.json())
        if is_verified is False:
            raise GatewaySignatureInvalid(response)

        return APIResponse(response, is_verified)

    def post(self, *args, **kwargs) -> APIResponse:
        """
        Call POST method on the resource.

        Returns:
            `APIResponse`
        """
        raise NotImplementedError()

    def get(self, *args, **kwargs) -> APIResponse:
        """
        Call GET method on the resource.

        Returns:
            `APIResponse`
        """
        raise NotImplementedError
