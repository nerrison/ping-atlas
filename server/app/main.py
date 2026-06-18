from fastapi import FastAPI
from app.db.database import Base,engine
from app.routes import groups
from app.db.init_db import init_db

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
    
    
