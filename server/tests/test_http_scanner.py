import uuid

from app.scanner.httpx_scanner import HttpScanner
from app.models.endpoint import EndpointType, HttpMethod, EndpointStatus
from app.scanner.result import ScanResult
from app.models.endpoint import Endpoint


class FakeResponse:
    status_code = 200


class FakeClient:

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def request(self, method, url):
        return FakeResponse()


def test_http_scanner_up(monkeypatch):

    monkeypatch.setattr(
        "httpx.Client",
        lambda timeout: FakeClient()
    )

    endpoint = Endpoint(
        id=uuid.uuid4(),
        type=EndpointType.HTTPS,
        url="example.com",
        method=HttpMethod.GET,
    )

    scanner = HttpScanner()

    result = scanner.scan(endpoint)

    assert result.endpoint_id == endpoint.id
    assert result.status == EndpointStatus.UP
    assert result.status_code == 200
    assert result.response_time is not None