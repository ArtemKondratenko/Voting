from __future__ import annotations

from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from sqlalchemy import select
from src.database import db
from werkzeug.security import check_password_hash
import typing

if typing.TYPE_CHECKING:
    from src.models.voting import Voting
    from src.models.voice import Voice


class User(db.Model, MappedAsDataclass):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    votings: Mapped[list[Voting]] = relationship("Voting", back_populates="user", init=False)
    voices: Mapped[list[Voice]] = relationship("Voice", back_populates="user", init=False)
    password: Mapped[str]

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id: int):
        return db.session.get(User, id)

    @staticmethod
    def get_user_by_with_password(name: str, password: str) -> User | None:
        user = db.session.scalars(
            select(User).where(User.name == name,
                               User.password == password)).first()
        return user

    def voice_for(self, voting_id: int) -> Voice | None:
        from src.models.voice import Voice
        return db.session.scalars(
            select(Voice).where(Voice.user_id == self.id,
                                Voice.voting_id == voting_id)).first()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True
