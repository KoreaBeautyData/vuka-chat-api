from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional

from database import schema
from database.database import get_db
from controller import fine_tune_controller

router = APIRouter(
    prefix="/api/fine-tune",
)


@router.get('', tags=['fine-tune'])
def get_fine_tune_list(session: Session = Depends(get_db),
                       page: Optional[int] = 1,
                       page_length: Optional[int] = 3,
                       refresh: Optional[bool] = False):
    response = fine_tune_controller.get_fine_tune_list(session=session,
                                                       page=page,
                                                       page_length=page_length,
                                                       refresh=refresh)
    return response


@router.get('/{fine_tune_id}', tags=['fine-tune'])
def get_fine_tune_detail(fine_tune_id: int,
                         session: Session = Depends(get_db)):
    response = fine_tune_controller.get_fine_tune_detail(fine_tune_id=fine_tune_id,
                                                         session=session)
    return response


@router.post('/convert', tags=['fine-tune'])
def post_convert_csv_to_jsonl(request: schema.FileSchema,
                              session: Session = Depends(get_db)):
    response = fine_tune_controller.post_convert_csv_to_jsonl(session=session,
                                                              request=request)
    return response


@router.post('/tuning', tags=['fine-tune'])
def post_fine_tuning(request: schema.FileSchema,
                     session: Session = Depends(get_db)):
    response = fine_tune_controller.post_fine_tuning(request=request,
                                                     session=session)
    return response


@router.get('/status', tags=['fine-tune'])
def get_fine_tuning_status(session: Session = Depends(get_db),
                           id: Optional[str] = None):
    response = fine_tune_controller.get_fine_tuning_status(session=session,
                                                           id=id)
    return response
