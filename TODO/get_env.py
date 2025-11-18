from functools import lru_cache
from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from . import config

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()


@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "ALGORITHM": settings.ALGORITHM,
        "SECRET_KEY": settings.SECRET_KEY,
        "ACCESS_TOKEN_EXPIRE_MINUTES": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    }