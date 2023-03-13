from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import schema
from database.database import get_db
from controller import faq_controller

router = APIRouter(
    prefix="/api/faq",
)


class FAQModel(BaseModel):
    question: str
    answer: str


@router.get('')
def get_faq(session: Session = Depends(get_db)):
    response = faq_controller.get_faq(session)
    return response

@router.post('')
def post_faq(request: FAQModel, session: Session = Depends(get_db)):
    response = faq_controller.post_faq(session=session,
                                       request=request)
    return response


