from sqlalchemy import Column, String, Integer

from base import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String)
    tg = Column(String)

    def __init__(self, name, phone_number, tg):
        self.name = name
        self.phone_number = phone_number
        self.th = tg
