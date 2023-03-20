import csv

from fastapi import APIRouter
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database.schema import *
from database.models import FAQ
from config import config


def get_faq(session: Session, page, page_length, keyword):
    response = DefaultModel()

    if page <= 0:
        page = 1
    else:
        page = page

    search_filter = []
    if keyword is not None:
        search_filter.append(or_(FAQ.question.like(f'%{keyword}%'),
                                 FAQ.answer.like(f'%{keyword}%')))

    faq_query = session.query(FAQ).filter(*search_filter)
    faq_list = faq_query.offset(page_length * (page - 1)).limit(page_length).all()

    response.result_data = {
        'faq_list': faq_list,
        'faq_count': faq_query.count()
    }
    return response


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

    data = []

    for faq in faq_list:
        data.append((f'{faq.question}{config.PROMPT_END_WITH3}', f' {faq.answer}'))

    file = open('csv_file/faq2.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()
    return data
