from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from config.error_handling import UnicornException

from router.faq import faq_api
from router.chat import chat_api
from router.fine_tune import fine_tune_api


tags_metadata = [
    {
        "name": "faq",
        "description": "",
    },
    {
        "name": "chat",
        "description": "",
    },
    {
        "name": "fine-tune",
        "description": "",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        content={'result_msg': exc.result_msg,
                 'result_code': exc.result_code})

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(faq_api.router)
app.include_router(chat_api.router)
app.include_router(fine_tune_api.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))


@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")
