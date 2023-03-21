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
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://3.35.21.66:8000",
    "http://3.35.21.66",
    "openai.codecom.co.kr:8000",
    "openai.codecom.co.kr",
    "http://openai.codecom.co.kr:8000/",
    "http://openai.codecom.co.kr/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
