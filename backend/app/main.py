import logging
from fastapi import FastAPI

from app.api.health import router as health_router
from app.db.base import Base
from app.db.session import engine

logger = logging.getLogger(__name__)
app = FastAPI(title="Admin Backend")


@app.on_event("startup")
def on_startup() -> None:
    if engine is None:
        logger.warning("DATABASE_URL not configured. Application will run without database.")
        return
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database connection established and tables created")
    except Exception as e:
        logger.warning(f"Failed to connect to database: {e}. Application will continue without database.")


app.include_router(health_router)
