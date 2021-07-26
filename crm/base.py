from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create an engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# create "Session" class
Session = sessionmaker(bind=engine)

# create a new session
session = Session()

Base = declarative_base()