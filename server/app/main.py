from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading

from app.routes import groups, endpoints, search, history, incidents
from app.core.bootstrap import load_environment

from app.scheduler.scheduler import Scheduler
from app.worker.worker import ScanWorker
from app.scanner.httpx_scanner import HttpScanner


load_environment()


@asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler = Scheduler(
        worker=ScanWorker(
            scanner=HttpScanner(),
            max_workers=10,
        ),
        interval=60,
    )

    thread = threading.Thread(
        target=scheduler.run,
        daemon=True,
    )

    thread.start()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "PingAtlas API running"}


@app.get("/db-test")
def db_test():
    from app.db.database import engine

    with engine.connect() as connection:
        return {"database": "connected"}


app.include_router(groups.router)
app.include_router(endpoints.group_router)
app.include_router(endpoints.endpoint_router)
app.include_router(search.router)
app.include_router(history.router)
app.include_router(incidents.router)