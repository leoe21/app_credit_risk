from fastapi import FastAPI
from api.capture import router as capture_router
from api.features import router as features_router
from core.config import settings

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

app.include_router(capture_router, prefix="/capture", tags=["Capture Data"])
app.include_router(features_router, prefix="/features", tags=["Features"])
