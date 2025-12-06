from fastapi import FastAPI
from .routers import auth, payments, users
from .database import engine, Base
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nexus API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(payments.router)
app.include_router(users.router)

@app.get("/")
def health_check():
    return {"status": "Healthy", "service":"nexus"}