import datetime

from pydantic import BaseModel


class FAQSchema(BaseModel):
    # id: int
    # status: int
    question: str
    answer: str
    # created_at: datetime.datetime
    # updated_at: datetime.datetime

    class Config:
        orm_mode = True