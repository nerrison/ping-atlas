from fastapi import FastAPI
from app.db.database import Base,engine


app = FastAPI()



@app.get("/")
def home():
    return {"message": "PingAtlas API running"}

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        return {"database": "connected"}
    

    
    
