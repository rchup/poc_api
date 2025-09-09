import os
import json
import pytest
from dotenv import load_dotenv

from modules.logger import TcLogger
from src.api.client import ApiClient
from src.api.config import ClientConfig


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    # Load variables from a .env file if present
    load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def enable_file_logging() -> None:
    TcLogger.generate_logs(
        level=os.getenv("API_LOG_LEVEL", "INFO"),
        detailed_logs=True,
        write_to_file=True,
        reports_dir=os.getenv("REPORTS_DIR", "reports"),
    )


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("API_BASE_URL", "https://httpbin.org")


@pytest.fixture(scope="session")
def api_client(base_url: str) -> ApiClient:
    default_headers_env = os.getenv("API_DEFAULT_HEADERS")
    default_headers = {}
    if default_headers_env:
        try:
            default_headers = json.loads(default_headers_env)
        except Exception:
            default_headers = {}

    config = ClientConfig(
        base_url=base_url,
        timeout_seconds=float(os.getenv("API_TIMEOUT", "10")),
        max_retries=int(os.getenv("API_MAX_RETRIES", "2")),
        backoff_factor=float(os.getenv("API_BACKOFF_FACTOR", "0.2")),
        verify_ssl=os.getenv("API_VERIFY_SSL", "true").lower() == "true",
        api_key=os.getenv("API_TOKEN"),
        default_headers=default_headers,
        log_level=os.getenv("API_LOG_LEVEL", "INFO"),
    )
    return ApiClient(config)
