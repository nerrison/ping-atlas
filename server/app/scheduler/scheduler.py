import time
import logging

from app.db.database import SessionLocal
from app.worker.worker import ScanWorker
from app.services.monitor import Monitor
from app.repositories.endpoint import EndpointRepository


logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(
        self,
        worker: ScanWorker,
        interval: int = 60,
    ):
        self.worker = worker
        self.interval = interval

    def run(self):
        logger.info("Scheduler started")

        while True:
            try:
                self.scan_cycle()

            except Exception:
                logger.exception("Scheduler cycle failed")

            time.sleep(self.interval)

    def scan_cycle(self):
        db = SessionLocal()

        try:
            endpoint_repo = EndpointRepository(db)
            monitor = Monitor(db)

            endpoints = endpoint_repo.list_all()

            if not endpoints:
                logger.info("No endpoints found")
                return

            logger.info(
                "Scanning %s endpoints",
                len(endpoints),
            )

            results = self.worker.run(endpoints)

            monitor.process_results(results)

            logger.info("Scan completed")

        finally:
            db.close()