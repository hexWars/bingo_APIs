from fastapi.responses import FileResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from starlette.templating import Jinja2Templates
from markdown2 import markdown
from os.path import isfile
from datetime import date
from core import *

app = FastAPI(title="bingo APIs", description="python sever powered by FastAPI")
app.add_middleware(GZipMiddleware, minimum_size=1024)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(experiment_router, prefix="/experiments", tags=["experiments"])
app.include_router(scale_router, prefix="/scales", tags=["scales"])
app.include_router(font_router, prefix="/fonts", tags=["fonts"])


@app.get("/", name="home_page")
async def home_page(request: Request):
    return Jinja2Templates("./data").TemplateResponse(
        "home.html",
        {
            "request": request,
            "readme": markdown(open("./readme.md", encoding="utf-8").read()),
            "date": f"—— today is {date.today()} ——"
        }
    )


class debugger:
    from loguru import logger
    debug = logger.debug
    info = logger.info
    warning = logger.warning
    error = logger.error
    critical = logger.critical

    @staticmethod
    @app.get("/refresh", tags=["debug"])
    def git_pull():
        from os import system
        debugger.info(system("git pull"))
        return RedirectResponse("/")

    @staticmethod
    @app.get("/debug/users", tags=["debug"])
    async def inspect_all_users():
        from core.users import User
        debugger.debug(f"{list(User.users.dict) = }")
        debugger.debug(f"{list(User.users.memo.keys()) = }")
        return list(User.users.dict.items())


@app.get("/{filepath:path}")
def get_static_assets(filepath: str):
    path = f"./data/{filepath}"
    if isfile(path):
        return FileResponse(path)
    else:
        raise HTTPException(404, f"fall back to static assets function and "
                                 f"{path!r} does not exists!")
