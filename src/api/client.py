from __future__ import annotations

import json as _json
from typing import Any, Dict, Optional

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import ClientConfig
from modules.logger import configure_logging, get_logger, redact_headers, log_timing


_logger = get_logger(__name__)


class ApiClient:
    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        configure_logging(config.log_level)
        self._session = requests.Session()
        retries = Retry(
            total=config.max_retries,
            backoff_factor=config.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
            raise_on_status=False,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)
        if config.default_headers:
            self._session.headers.update(config.default_headers)
        if config.api_key:
            self._session.headers.update({"Authorization": f"Bearer {config.api_key}"})

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self._config.base_url.rstrip('/')}/{path.lstrip('/')}"

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Response:
        url = self._url(path)
        request_headers: Dict[str, str] = {}
        if headers:
            request_headers.update(headers)

        _logger.debug(
            "HTTP %s %s params=%s headers=%s body=%s",
            method.upper(),
            url,
            params,
            redact_headers({**self._session.headers, **request_headers} if self._session.headers else request_headers),
            _json.dumps(json)[:512] if json is not None else None,
        )
        with log_timing(_logger, f"{method.upper()} {url}"):
            response = self._session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                headers=request_headers or None,
                timeout=timeout or self._config.timeout_seconds,
                verify=self._config.verify_ssl,
            )
        return response

    def get(self, path: str, **kwargs: Any) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        return self.request("DELETE", path, **kwargs)

    # JSON helpers
    def get_json(self, path: str, **kwargs: Any) -> Any:
        resp = self.get(path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def post_json(self, path: str, *, json: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        resp = self.post(path, json=json, **kwargs)
        resp.raise_for_status()
        return resp.json()
