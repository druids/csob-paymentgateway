import json
from itertools import chain
from typing import Iterable, Tuple, Dict, Optional, List, Any
from urllib.parse import urljoin

import requests

from csob.api_response import APIResponse
from csob.crypto import get_signature, get_url_signature, verify_signature
from csob.exceptions import HTTP_ERROR_CSOB_EXCEPTIONS, GatewaySignatureInvalid
from csob.utils import get_dttm


class CSOBResource:
    url: str
    url_args: Optional[Tuple[str]] = None

    request_signature: Tuple[str]
    optional_request_signature: Tuple[str] = tuple()
    response_signature: Tuple[str]
    optional_response_signature: Tuple[str] = tuple()

    _base_url: str
    _gateway_key: str
    _private_key: str
    merchant_id: str
    session: requests.Session
    raise_exception = True

    def __init__(self, base_url: str, merchant_id: str, gateway_key: str, private_key: str,
                 session: requests.Session = requests.Session(),
                 raise_exception: bool = True):
        self._gateway_key = gateway_key
        self._private_key = private_key
        self.raise_exception = raise_exception
        self.merchant_id = merchant_id
        self._base_url = base_url
        self.session = session

    def get_base_json(self) -> dict:
        return {
            'merchantId': self.merchant_id,
            'dttm': get_dttm(),
        }

    def get_url(self) -> str:
        """
        Join base url supplied by APIClient and resource url.

        Returns:
            URL
        """
        return urljoin(self._base_url, self.url)

    def get_url_args(self) -> Tuple:
        if self.url_args is not None:
            return self.url_args
        return self.request_signature + ('signature',)

    def _filter_signature_str_keys(self, local_json: Dict) -> List[str]:
        """
        Filter which json keys we can use to construct signature.

        Args:
            local_json: The json from which the signature will be constructed.

        Returns:
            List - of json keys
        """
        return [i for i in self.request_signature if
                (i not in self.optional_request_signature or i in local_json.keys())
                ]

    @staticmethod
    def _convert_json_item_signature(item: Any) -> List[str]:
        """
        Converts json item into it's str form.

        Args:
            item: An item from json.

        Returns:
            List - of string representations
        """
        if isinstance(item, list):  # Cart list of dicts
            for j in item:
                return [str(k) for k in j.values()]
        elif item is True:
            return ['true']
        elif item is False:
            return ['false']
        else:
            return [str(item)]

    def _construct_signature_str(self, local_json: Dict) -> str:
        """
        From json constructs signature str.

        Args:
            local_json: JSON from which to get the signature str.

        Returns:
            Signature str
        """
        return "|".join(chain.from_iterable([
            self._convert_json_item_signature(local_json[i])
            for i in self._filter_signature_str_keys(local_json)
        ]))

    def _construct_verify_signature_str(self, local_json: Dict) -> str:
        """
        From response json constructs signature str.

        Args:
            local_json: JSON from which to get the signature str.

        Returns:
            Signature str
        """
        return "|".join([str(local_json[i]) for i in self.response_signature if
                         (i not in self.optional_response_signature or i in local_json.keys())])

    def construct_url(self, local_json: Dict) -> str:
        """
        Construct whole url using url_args and local_json.

        Args:
            local_json: JSON from which to get the data for url.

        Returns:
            URL
        """
        url_str = ""

        for arg in self.get_url_args():
            if arg == "merchantId":
                url_str = url_str + str(self.merchant_id) + "/"
            elif arg == "signature":
                url_str = url_str + str(self.get_url_signature(local_json)) + "/"
            else:
                url_str = url_str + str(local_json[arg]) + "/"

        return urljoin(self.get_url(), url_str[:-1])

    def get_signature(self, local_json: Dict) -> str:
        """
        Construct signature str and calls `csob.crypto.get_signature`.

        Args:
            local_json: JSON to be sent from which the signature str is built

        Returns:
            Signature
        """
        return get_signature(self._private_key, self._construct_signature_str(local_json))

    def get_url_signature(self, local_json: Dict) -> str:
        """
        Construct signature str and calls `csob.crypto.get_signature`.

        Args:
            local_json: JSON to be sent from which the signature str is built

        Returns:
            Signature
        """
        return get_url_signature(self._private_key, self._construct_signature_str(local_json))

    def verify_signature(self, local_json: Dict) -> bool:
        """
        Construct signature str for response and calls `csob.crypto.verify_signature`

        Args:
            local_json: The JSON to be verified
            json['signature']: The signature to be verified.

        Returns:
            bool
        """
        return verify_signature(
            self._gateway_key,
            self._construct_verify_signature_str(local_json), local_json['signature']
        )

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

        is_verified = self.verify_signature(response.json())
        if is_verified is False and self.raise_exception:
            raise GatewaySignatureInvalid(response)

        return APIResponse(response, is_verified=is_verified)

    def _sign_json(self, local_json: Dict) -> Dict:
        local_json['signature'] = self.get_signature(local_json)
        return local_json

    def post(self, *args, **kwargs) -> APIResponse:
        """
        Call POST method on the resource.

        Returns:
            `APIResponse`
        """
        raise NotImplementedError()

    def _sign_and_post(self, local_json: Dict) -> APIResponse:
        return self.parse_response(self.session.post(self.get_url(), data=json.dumps(self._sign_json(local_json))))

    def get(self, *args, **kwargs) -> APIResponse:
        """
        Call GET method on the resource.

        Returns:
            `APIResponse`
        """
        raise NotImplementedError

    def _get(self, url: str) -> APIResponse:
        return self.parse_response(self.session.get(url))

    def _construct_url_and_get(self, local_json: Dict) -> APIResponse:
        return self._get(self.construct_url(local_json))

    def put(self, *args, **kwargs) -> APIResponse:
        """
        Call PUT method on the resource.

        Returns:
            `APIResponse`
        """
        raise NotImplementedError

    def _sign_and_put(self, local_json: Dict) -> APIResponse:
        return self.parse_response(self.session.put(self.get_url(), data=json.dumps(self._sign_json(local_json))))
