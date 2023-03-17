from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database.database import get_db
from controller import chat_controller

router = APIRouter(
    prefix="/api/chat",
)


@router.get('')
def get_chat(question: Optional[str] = None,
             session: Session = Depends(get_db)):
    response = chat_controller.get_chat(question=question,
                                        session=session)
    return response


@router.get('/tuning')
def get_fine_tuning(session: Session = Depends(get_db)):
    response = chat_controller.fine_tuning(session=session)
    return response
