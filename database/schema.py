import datetime

from pydantic import BaseModel


class DefaultModel(BaseModel):
    class Config:
        orm_mode = True


class FAQSchema(DefaultModel):
    id: int
    status: int
    question: str
    answer: str
    created_at: datetime.datetime
    updated_at: datetime.datetime