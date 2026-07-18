import time
import httpx

from app.models.endpoint import EndpointStatus
from .result import ScanResult


class HttpScanner:
    def scan(self, endpoint):
        start = time.perf_counter()

        url = f"{endpoint.type.value.lower()}://{endpoint.url}"

        try:
            with httpx.Client(timeout=10) as client:
                response = client.request(
                    method=endpoint.method.value,
                    url=url,
                )

            latency_ms = int((time.perf_counter() - start) * 1000)

            if response.status_code >= 500:
                status = EndpointStatus.DOWN
            elif response.status_code >= 400:
                status = EndpointStatus.DEGRADED
            elif latency_ms > 3000:
                status = EndpointStatus.DEGRADED
            else:
                status = EndpointStatus.UP

            return ScanResult(
                endpoint_id=endpoint.id,
                status=status,
                status_code=response.status_code,
                response_time=latency_ms,
                message=None,
            )

        except httpx.TimeoutException:
            return ScanResult(
                endpoint_id=endpoint.id,
                status=EndpointStatus.DOWN,
                status_code=None,
                response_time=None,
                message="Request timed out",
            )

        except httpx.RequestError as exc:
            return ScanResult(
                endpoint_id=endpoint.id,
                status=EndpointStatus.DOWN,
                status_code=None,
                response_time=None,
                message=str(exc),
            )