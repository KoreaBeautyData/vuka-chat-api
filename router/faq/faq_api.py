from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from database import schema
from database.database import get_db
from controller import faq_controller

router = APIRouter(
    prefix="/api/faq",
)


@router.get('', tags=['faq'], status_code=200)
def get_faq(session: Session = Depends(get_db),
            page: Optional[int] = 1,
            page_length: Optional[int] = 3,
            keyword: Optional[str] = None):
    response = faq_controller.get_faq(session=session,
                                      page=page,
                                      page_length=page_length,
                                      keyword=keyword)
    return response


@router.post('', tags=['faq'], response_model=schema.FAQSchema)
def post_faq(request: schema.FAQCreateSchema,
             session: Session = Depends(get_db)):
    response = faq_controller.post_faq(session=session,
                                       request=request)
    return response


@router.put('/{faq_id}', tags=['faq'], response_model=schema.FAQSchema)
def put_faq_detail(faq_id: int,
                   request: schema.FAQCreateSchema,
                   session: Session = Depends(get_db)):
    response = faq_controller.put_faq_detail(faq_id=faq_id,
                                             session=session,
                                             request=request)
    return response


@router.get('/{faq_id}', tags=['faq'], status_code=200)
def get_faq_detail(faq_id: int,
                   session: Session = Depends(get_db)):
    response = faq_controller.get_faq_detail(faq_id=faq_id,
                                             session=session)
    return response


@router.delete('/{faq_id}', tags=['faq'])
def delete_faq_detail(faq_id: int,
                      session: Session = Depends(get_db)):
    response = faq_controller.delete_faq_detail(faq_id=faq_id,
                                                session=session)
    return response


@router.post('/csv', tags=['faq'])
def post_faq_csv(request: schema.FileSchema,
                 session: Session = Depends(get_db)):
    response = faq_controller.post_faq_csv(request=request,
                                           session=session)
    return response