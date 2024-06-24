from __future__ import annotations

from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from sqlalchemy import select
from sqlalchemy.sql.schema import ForeignKey
from typing import Iterable
from src.database import db

import typing

if typing.TYPE_CHECKING:
    from src.models.user import User
    from src.models.voice import Voice


class Voting(db.Model, MappedAsDataclass):
    __tablename__ = "voting"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User", back_populates="votings", init=False)
    voices: Mapped[list[Voice]] = relationship("Voice", back_populates="voting", init=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id: int):
        return db.session.get(Voting, id)

    @staticmethod
    def get_all() -> Iterable[Voting]:
        from src.models.user import User
        votings = db.session.scalars(select(Voting)).all()
        return list(votings)

    def get_vote_count(self):
        num_votes_for = 0
        num_votes_aganist = 0

        for voice in self.voices:
            if voice.voice_status:
                num_votes_for += 1
            else:
                num_votes_aganist += 1

        return num_votes_for, num_votes_aganist

