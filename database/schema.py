from pydantic import BaseModel


class DefaultModel(BaseModel):
    result_code: int = 200
    result_msg: str = "성공"
    result_data: dict = {}

    class Config:
        orm_mode = True


class FAQSchema(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True


class FAQCreateSchema(BaseModel):
    question: str
    answer: str

    class Config:
        orm_mode = True


class FAQDetailSchema(DefaultModel):
    id: int
    question: str
    answer: str


class ChatSchema(BaseModel):
    question: str
    fine_tuned_model: str


class ChatDBSchema(BaseModel):
    question: str


class FileSchema(BaseModel):
    filename: str

    class Config:
        orm_mode = True


class FineTuneModelSchema(BaseModel):
    fine_tuned_model: str

    class Config:
        orm_mode = True


class DefaultReqModel(BaseModel):
    class Config:
        orm_mode = True

class DefaultResModel(BaseModel):
    class Config:
        orm_mode = True
    result: str = "Y"
    msg: str = None


class get_socialinfo_req(DefaultReqModel):
    social: str = None
    socialkey: str = None

class get_socialinfo_res(DefaultResModel):
    vkid: str = None

class get_socialinfo_all_req(DefaultReqModel):
    vkid: str = None

class get_socialinfo_all_res(DefaultResModel):
    kakao: str = None

class post_socialinfo_add_req(DefaultReqModel):
    vkid: str = None
    social: str = None
    socialkey: str = None
