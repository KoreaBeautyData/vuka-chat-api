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
    faq.question = question
    faq.answer = answer
    session.add(faq)
    session.commit()
    return faq


def post_faq_csv(session: Session):
    faq_list = session.query(FAQ).all()

    data = [('prompt', 'completion')]

    for faq in faq_list:
        data.append((faq.question, faq.answer))

    file = open('csv_file/faq.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()
    return data