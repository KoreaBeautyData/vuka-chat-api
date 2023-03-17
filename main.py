from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from router.faq import faq_api
from router.chat import chat_api

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://3.35.21.66:8000",
    "http://3.35.21.66",
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
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))


@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")