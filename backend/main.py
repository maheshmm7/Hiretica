from fastapi import FastAPI

app = FastAPI(title="Hiretica API", version="1.0.0")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Hiretica API"}
