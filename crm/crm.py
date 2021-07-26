import tkinter as tk
import datetime

from base import Base, Session, session, engine
from client import Client
from employee import Employee
from application import Application
from app import App


# generate database schema
Base.metadata.create_all(engine)


app1 = Application(creation_date=datetime.date(day=25, month=12, year=2000), status='открыта', type='Ремонт')
app2 = Application(creation_date=datetime.date(day=1, month=2, year=3), status='в работе', type='Обслуживание')
app3 = Application(creation_date=datetime.date(day=11, month=9, year=2021), status='закрыта', type='Консультация')
session.add(app1)
session.add(app2)
session.add(app3)
session.commit()
session.close()

# apps = session.query(Application).all()
#
# for app in apps:
#     print(repr(app))


if __name__ == "__main__":
    app = App()
    app.mainloop()
