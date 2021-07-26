from sqlalchemy import Column, String, Integer

from base import Base


class Client(Base):
    """ORM type clients SQL table"""
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    tg = Column(String)

    def __init__(self, name, phone_number, tg):
        self.name = name
        self.phone_number = phone_number
        self.tg = tg

    def attribute_list(self):
        return [self.name, self.phone_number, self.tg]
