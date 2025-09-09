from modules.logger import TcLogger
from src.api.client import ApiClient


def test_get_status_ok(api_client: ApiClient) -> None:
    TcLogger.get_log().log_test_name("test_get_status_ok")
    resp = api_client.get("/status/200")
    assert resp.status_code == 200


def test_post_json_echo(api_client: ApiClient) -> None:
    TcLogger.get_log().log_test_name("test_post_json_echo")
    payload = {"hello": "world"}
    body = api_client.post_json("/anything", json=payload)
    assert body["json"] == payload


def test_default_headers_roundtrip(api_client: ApiClient) -> None:
    TcLogger.get_log().log_test_name("test_default_headers_roundtrip")
    # httpbin echoes headers in response['headers']
    resp = api_client.get("/anything")
    assert resp.status_code == 200
    echoed = resp.json()["headers"]
    # Authorization header could be set; just ensure presence of a User-Agent from requests
    assert "User-Agent" in echoed
