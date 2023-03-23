from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import SOCIAL
from app.database import schema
from app.common.function import AESCipher

# vkid에 맞는 소셜정보조회
def get_socialinfo(request, session: Session):
    social = request.social
    socialkey = request.socialkey
    response = schema.get_socialinfo_res()

    if social == "1":
        get_list = session.query(SOCIAL.vkid).filter(SOCIAL.kakao==socialkey).all()
        if len(get_list) > 0:
            vkid = get_list[0].vkid
            # response.vkid = AESCipher().encrypt_str(str(vkid))
            response.vkid = str(vkid)
        else:
            response.result = "N"
            response.msg = "조회되는 정보가 없습니다."
    else:
        # 소셜정보 오류
        response.result = "N"
        response.msg = "소셜정보 오류"

    return response


# 소셜정보 전체조회
def get_socialinfo_all(request, session: Session):
    response = schema.get_socialinfo_all_res()
    vkid = request.vkid
    #vkid = AESCipher().decrypt_str(request.vkid)

    get_list = session.query(SOCIAL).filter(SOCIAL.vkid == vkid).all()

    if len(get_list) > 0:
        response.kakao = get_list[0].kakao
    else:
        response.result = "N"
        response.msg = "조회되는 정보가 없습니다."
    return response


# 소셜정보 추가
def post_socialinfo_add(request, session: Session):
    response = schema.DefaultResModel()
    vkid = request.vkid
    socialkey = request.socialkey
    get_list = session.query(SOCIAL).filter(SOCIAL.vkid == vkid).first()

    if get_list is None:
        social = SOCIAL()

        social.vkid = vkid

        if request.social == "1":
            get_list.kakao = None if len(socialkey) == 0 else socialkey
        else:
            response.result = "N"
            response.msg = "입력값이 잘못되었습니다."

        session.add(social)
    else:
        if request.social == "1":
            get_list.kakao = None if len(socialkey) == 0 else socialkey
        else:
            response.result = "N"
            response.msg = "입력값이 잘못되었습니다."

    session.commit()

    return response