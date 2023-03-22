import csv

from sqlalchemy import or_
from sqlalchemy.orm import Session

from database.schema import *
from database.models import FAQ
from config.config import *
from config.error_handling import UnicornException


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

    faq_query = session.query(FAQ).filter(FAQ.status >= STATUS_INACTIVE,
                                          *search_filter).order_by(FAQ.id.asc())
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
    session.add(faq)
    session.flush()

    faq.question = question
    faq.answer = answer

    session.commit()
    return faq


def put_faq_detail(faq_id, request, session: Session):
    question = request.question
    answer = request.answer

    faq = session.query(FAQ).filter(FAQ.status >= STATUS_INACTIVE,
                                    FAQ.id == faq_id).first()
    if faq is None:
        raise UnicornException(result_msg=ERROR_DATA_NOT_EXIST[1],
                               result_code=ERROR_DATA_NOT_EXIST[0])

    faq.question = question
    faq.answer = answer
    session.commit()
    return faq


def get_faq_detail(faq_id, session: Session):
    response = DefaultModel()
    faq = session.query(FAQ).filter(FAQ.id == faq_id,
                                    FAQ.status >= STATUS_INACTIVE).first()
    if faq is None:
        raise UnicornException(result_msg=ERROR_DATA_NOT_EXIST[1],
                               result_code=ERROR_DATA_NOT_EXIST[0])

    response.result_data = {
        'faq': faq
    }
    return response


def delete_faq_detail(faq_id, session: Session):
    response = DefaultModel()

    faq = session.query(FAQ).filter(FAQ.id == faq_id).first()
    if faq is None:
        raise UnicornException(result_msg=ERROR_DATA_NOT_EXIST[1],
                               result_code=ERROR_DATA_NOT_EXIST[0])

    faq.status = STATUS_DELETE
    session.commit()
    return response


def post_faq_csv(session: Session):
    faq_list = session.query(FAQ).filter(FAQ.status >= STATUS_INACTIVE).all()

    data = []

    for faq in faq_list:
        data.append((f'{faq.question}\n뷰카프로 ->\n', f' {faq.answer} \n##\n'))

    file = open('./faq.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()
    return file.name
