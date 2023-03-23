from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime

from app.database.database import Base


class SOCIAL(Base):
    __tablename__ = 'socialinfo'

    vkid = Column(Integer, primary_key=True, index=True)
    kakao = Column(Text, default=None)

