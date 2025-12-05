from fastapi import FastAPI


app = FastAPI(title="Nexus API")

@app.get("/")
def health_check():
    return {"status": "Healthy", "service":"nexus"}