from pydantic import BaseModel


class DefaultModel(BaseModel):
    class Config:
        orm_mode = True


class FAQSchema(DefaultModel):
    id: int
    question: str
    answer: str