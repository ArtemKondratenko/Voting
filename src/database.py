from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing_extensions import Self

class Base(DeclarativeBase, MappedAsDataclass):

  def save(self):
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def get(id: int):
    return db.session.get(Self, id)

db = SQLAlchemy(model_class=Base)


def create_tables(app):
  with app.app_context():
    # db.drop_all()
    db.create_all()