from __future__ import annotations

from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from sqlalchemy import select
from sqlalchemy.sql.schema import ForeignKey
from typing import Iterable
from src.database import db

import typing

if typing.TYPE_CHECKING:
    from src.models.user import User
    from src.models.voting import Voting


class Voice(db.Model, MappedAsDataclass):
    __tablename__ = "voice"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    voting_id: Mapped[int] = mapped_column(ForeignKey("voting.id"))
    voting: Mapped[Voting] = relationship("Voting", back_populates="voices", init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User", back_populates="voices", init=False)
    voice_status: Mapped[bool] = mapped_column(default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()






