from pydantic import BaseModel


class DefaultModel(BaseModel):
    result_code: int = 200
    result_msg: str = "성공"
    result_data: dict = {}

    class Config:
        orm_mode = True


class FAQSchema(DefaultModel):
    id: int
    question: str
    answer: str