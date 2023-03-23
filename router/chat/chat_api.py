from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database import schema
from database.database import get_db
from controller import chat_controller

router = APIRouter(
    prefix="/api/chat",
)


@router.post('', tags=['chat'])
def post_chat(request: schema.ChatSchema,
              session: Session = Depends(get_db),):
    response = chat_controller.post_chat(request=request,
                                         session=session)
    return response


@router.post('/db', tags=['chat'])
def post_chat_db(request: schema.ChatDBSchema,
                 session: Session = Depends(get_db)):
    response = chat_controller.post_chat_db(request=request,
                                            session=session)
    return response