from sys import path
from functools import cache
from fastapi import FastAPI
from fastapi.responses import FileResponse
from core import experiment_router, scale_router
from fastapi.middleware.gzip import GZipMiddleware

path.append("./data")
app = FastAPI(title="bingo APIs", description="python sever powered by FastAPI")
app.add_middleware(GZipMiddleware, minimum_size=1024)

app.include_router(scale_router, prefix="/scales", tags=["scales"])
app.include_router(experiment_router, prefix="/experiments", tags=["experiments"])


@app.get("/{file}", name="get_static_file")
@cache
def get_static_file(file: str):
    return FileResponse(f"./data/{file or 'home.html'}")
