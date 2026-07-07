from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes import groups, endpoints, search, history, incidents
from app.core.bootstrap import load_dotenv

load_dotenv()

app = FastAPI()


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