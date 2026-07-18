import uuid

from app.worker.worker import ScanWorker
from app.scanner.result import ScanResult
from app.models.endpoint import EndpointStatus


class FakeScanner:

    def scan(self, endpoint):
        return ScanResult(
            endpoint_id=endpoint.id,
            status=EndpointStatus.UP,
            status_code=200,
            response_time=100,
            message=None,
        )


class FakeEndpoint:
    def __init__(self):
        self.id = uuid.uuid4()


def test_worker_scans_all_endpoints():

    endpoints = [
        FakeEndpoint(),
        FakeEndpoint(),
        FakeEndpoint(),
    ]

    worker = ScanWorker(
        scanner=FakeScanner(),
        max_workers=3,
    )

    results = worker.run(endpoints)

    assert len(results) == 3

    endpoint_ids = {
        result.endpoint_id
        for result in results
    }

    assert endpoint_ids == {
        endpoint.id
        for endpoint in endpoints
    }


def test_worker_returns_scan_results():

    endpoint = FakeEndpoint()

    worker = ScanWorker(
        scanner=FakeScanner()
    )

    results = worker.run([endpoint])

    result = results[0]

    assert isinstance(result, ScanResult)
    assert result.endpoint_id == endpoint.id
    assert result.status == EndpointStatus.UP
    assert result.status_code == 200
    assert result.response_time == 100