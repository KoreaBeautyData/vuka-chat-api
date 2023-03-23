import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from app.router.auth import auth_api
from app.router.social import social_api


app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(auth_api.router)
app.include_router(social_api.router)
