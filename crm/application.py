from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class Application(Base):
    """ORM type applications SQL table"""

    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    creation_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    type = Column(String, nullable=False)

    client_id = Column(Integer, ForeignKey('clients.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))

    client = relationship("Client", backref=backref("application", uselist=False))
    employee = relationship("Employee", backref=backref("application", uselist=False))


    def attribute_list(self):
        return [self.creation_date, self.status, self.type, self.client.name, self.employee.name]

    def __repr__(self):
        rep = str(self.creation_date) + ' ' + self.status + ' ' + self.type
        return rep
