from base import Base, engine
from app import App


# generate database schema
Base.metadata.create_all(engine)


if __name__ == "__main__":
    app = App()
    app.mainloop()
