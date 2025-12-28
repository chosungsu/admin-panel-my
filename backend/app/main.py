from fastapi import FastAPI

from app.api.health import router as health_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Admin Backend")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
