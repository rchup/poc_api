import os
import pytest

from taf import ApiClient, ClientConfig


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("API_BASE_URL", "https://httpbin.org")


@pytest.fixture(scope="session")
def api_client(base_url: str) -> ApiClient:
    config = ClientConfig(
        base_url=base_url,
        timeout_seconds=float(os.getenv("API_TIMEOUT", "10")),
        max_retries=int(os.getenv("API_MAX_RETRIES", "2")),
        backoff_factor=float(os.getenv("API_BACKOFF_FACTOR", "0.2")),
        verify_ssl=os.getenv("API_VERIFY_SSL", "true").lower() == "true",
        api_key=os.getenv("API_TOKEN"),
    )
    return ApiClient(config)
