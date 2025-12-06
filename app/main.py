from fastapi import FastAPI
from .routers import auth
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nexus API")

app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"status": "Healthy", "service":"nexus"}