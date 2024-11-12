from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    author: Mapped[str] = mapped_column(String)
    rating: Mapped[int] = mapped_column(Integer)
    def get_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    def get_name(self):
        return {"username":self.username, "email":self.email}

