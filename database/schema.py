from pydantic import BaseModel


class DefaultModel(BaseModel):
    result_code: int = 200
    result_msg: str = "성공"
    result_data: dict = {}

    class Config:
        orm_mode = True


class FAQSchema(BaseModel):
    question: str
    answer: str


class FAQDetailSchema(DefaultModel):
    id: int
    question: str
    answer: str


class ChatSchema(BaseModel):
    question: str
