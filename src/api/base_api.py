# pylint: disable=logging-fstring-interpolation, unidiomatic-typecheck
"""
Module that represents base api functionality
"""

from typing import Any, Dict, Optional

from requests import Response

from .client import ApiClient
from modules.logger import get_logger


_logger = get_logger(__name__)


class BaseApi:
    """
    Base mixin providing common HTTP methods and response helpers for APIs.

    Usage:
        client = ApiClient(config)
        users = BaseApi(client, "/users")
        resp = users.get()
    """

    def __init__(self, client: ApiClient, path: str) -> None:
        self._client = client
        self._path = path

    def _full_path(self, path: Optional[str] = None) -> str:
        if not path:
            return self._path
        return f"{self._path.rstrip('/')}/{path.lstrip('/')}"

    # HTTP methods
    def get(
        self,
        path: Optional[str] = None,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._client.get(self._full_path(path or ""), params=params, headers=headers, **kwargs)

    def post(
        self,
        path: Optional[str] = None,
        *,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._client.post(self._full_path(path or ""), json=json, headers=headers, **kwargs)

    def patch(
        self,
        path: Optional[str] = None,
        *,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._client.patch(self._full_path(path or ""), json=json, headers=headers, **kwargs)

    def put(
        self,
        path: Optional[str] = None,
        *,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._client.put(self._full_path(path or ""), json=json, headers=headers, **kwargs)

    def delete(
        self,
        path: Optional[str] = None,
        *,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Response:
        return self._client.delete(self._full_path(path or ""), json=json, headers=headers, **kwargs)

    # Response helpers
    @staticmethod
    def get_response_json(response: Response) -> Any:
        """
        Return parsed JSON body or raise ValueError if invalid JSON.
        """
        return response.json()

    def is_json(self, response: Response) -> bool:
        try:
            self.get_response_json(response)
            return True
        except Exception:
            return False

    def is_array(self, response: Response) -> bool:
        try:
            return isinstance(self.get_response_json(response), list)
        except Exception:
            return False

    def is_object_present_in_array(self, response: Response) -> bool:
        try:
            return bool(self.get_response_json(response))
        except Exception:
            return False

    def get_object_by_index(self, response: Response, index: int = 0) -> Dict[str, Any]:
        data = self.get_response_json(response)
        if not isinstance(data, list):
            raise TypeError("Response JSON is not a list")
        return data[index]

    @staticmethod
    def validate_params(obj: Dict[str, Any], *required_keys: str) -> bool:
        return set(required_keys).issubset(set(obj.keys()))

    @staticmethod
    def validate_types(data: Dict[str, Any], **types: type) -> bool:
        for key, expected_type in types.items():
            if key not in data or not isinstance(data[key], expected_type):
                return False
        return True

    def get_message(self, response: Response) -> Optional[str]:
        body = self.get_response_json(response)
        return body.get("message") if isinstance(body, dict) else None

    def get_detail(self, response: Response) -> Optional[str]:
        body = self.get_response_json(response)
        return body.get("detail") if isinstance(body, dict) else None

    def get_msg(self, response: Response, index: int = 0) -> Optional[str]:
        body = self.get_response_json(response)
        if isinstance(body, dict) and isinstance(body.get("detail"), list):
            item = body["detail"][index]
            if isinstance(item, dict):
                return item.get("msg")
        return None
