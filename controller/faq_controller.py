import csv

from fastapi import APIRouter
from sqlalchemy.orm import Session

from models import FAQ

router = APIRouter(
    prefix="/api/faq",
)


def get_faq(session: Session):
    faq_list = session.query(FAQ).all()
    return faq_list


def post_faq(request, session: Session):
    question = request.question
    answer = request.answer

    faq = FAQ()
    # faq.id = 3
    faq.question = question
    faq.answer = answer
    session.add(faq)
    session.commit()
    return faq
