from taf import ApiClient


def test_get_status_ok(api_client: ApiClient) -> None:
    resp = api_client.get("/status/200")
    assert resp.status_code == 200


def test_get_json_echo(api_client: ApiClient) -> None:
    payload = {"hello": "world"}
    resp = api_client.post("/anything", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["json"] == payload
