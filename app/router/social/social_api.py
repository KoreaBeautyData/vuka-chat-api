from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import schema
from app.database.database import get_db
from app.controller import social_controller


router = APIRouter(
    prefix="/api/social",
)


# 소셜정보조회
# param : social, socialkey
# return : vkid
@router.post('/socialinfo', response_model=schema.get_socialinfo_res)
def get_socialinfo(request: schema.get_socialinfo_req,session: Session = Depends(get_db)):
    response = social_controller.get_socialinfo(request=request,session=session)
    return response


# 소셜정보 전체조회
# param : vkid
# return : 소셜로그인전체 정보
@router.post('/socialinfoall', response_model=schema.get_socialinfo_all_res)
def get_socialinfo_all(request: schema.get_socialinfo_all_req,session: Session = Depends(get_db)):
    response = social_controller.get_socialinfo_all(request=request,session=session)
    return response


# 소셜정보 추가
# param : vkid, social, socialkey
# return : 성공, 실패
@router.post('/socialinfoadd')
def post_socialinfo_add(request: schema.post_socialinfo_add_req, session: Session = Depends(get_db)):
    response = social_controller.post_socialinfo_add(request=request, session=session)
    return response