from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import schema
from database.database import get_db
from controller import faq_controller

router = APIRouter(
    prefix="/api/faq",
)


@router.get('', response_model=List[schema.FAQSchema])
def get_faq(session: Session = Depends(get_db)):
    response = faq_controller.get_faq(session)
    return response


@router.post('')
def post_faq(request: schema.FAQSchema, session: Session = Depends(get_db)):
    response = faq_controller.post_faq(session=session,
                                       request=request)
    return response


@router.post('/csv')
def post_faq_csv(session: Session = Depends(get_db)):
    response = faq_controller.post_faq_csv(session=session)
    return response