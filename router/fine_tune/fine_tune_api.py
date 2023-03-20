from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional

from database import schema
from database.database import get_db
from controller import fine_tune_controller

router = APIRouter(
    prefix="/api/fine-tune",
)


@router.get('')
def get_fine_tune_list():
    response = fine_tune_controller.get_fine_tune_list()
    return response


@router.post('/convert')
def post_convert_csv_to_jsonl():
    response = fine_tune_controller.post_convert_csv_to_jsonl()
    return response


@router.post('/tuning')
def post_fine_tuning(session: Session = Depends(get_db)):
    response = fine_tune_controller.post_fine_tuning(session=session)
    return response


@router.get('/status')
def get_fine_tuning_status(session: Session = Depends(get_db),
                           id: Optional[str] = None):
    response = fine_tune_controller.get_fine_tuning_status(session=session,
                                                           id=id)
    return response
