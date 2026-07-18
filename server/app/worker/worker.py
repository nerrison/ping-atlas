from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Protocol

from app.scanner.result import ScanResult


class ScannerProtocol(Protocol):
    def scan(self, endpoint) -> ScanResult:
        ...


class ScanWorker:
    def __init__(
        self,
        scanner: ScannerProtocol,
        max_workers: int = 10,
    ):
        self.scanner = scanner
        self.max_workers = max_workers

    def run(self, endpoints) -> list[ScanResult]:
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(
                    self.scanner.scan,
                    endpoint
                )
                for endpoint in endpoints
            ]

            for future in as_completed(futures):
                results.append(future.result())

        return results