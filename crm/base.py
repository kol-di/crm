from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create an engine
engine = create_engine("sqlite:///:db", echo=True, future=True)

# create base class
Base = declarative_base()

# Create all the tables in the database which are
# defined by Base's subclasses
Base.metadata.create_all(engine)

# Construct a sessionmaker factory object
# and bind the sessionmaker to engine
Session = sessionmaker(bind=engine)

# create a new session
session = Session()
