from email.policy import default
from sqlalchemy import Boolean, Column, Integer, LargeBinary, String
from database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String, index=True)
    data = Column(LargeBinary)
    category = Column(Boolean, default=False) 

  