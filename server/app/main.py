from fastapi import FastAPI
from app.db.database import Base,engine
from app.db.init_db import init_db

from app.routes import groups
from app.routes import endpoints
from app.routes import search
from app.routes import history
from app. routes import incidents


app = FastAPI()

init_db()

@app.get("/")
def home():
    return {"message": "PingAtlas API running"}

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        return {"database": "connected"}
    
app.include_router(groups.router)

app.include_router(endpoints.group_router)
app.include_router(endpoints.endpoint_router)
app.include_router(search.router)
app.include_router(history.router)
app.include_router(incidents.router)
    
    
