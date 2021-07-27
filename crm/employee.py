from sqlalchemy import Column, String, Integer

from base import Base


class Employee(Base):
    """ORM type employees SQl table"""

    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String)

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def attribute_list(self):
        return [self.name, self.phone_number, self.id]
