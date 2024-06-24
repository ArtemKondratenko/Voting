from src.models.user import User
from src.models.voting import Voting
from flask_login import LoginManager
from flask import session

login_manager = LoginManager()

login_manager.login_view = "register.get_login" # type: ignore

@login_manager.user_loader
def load_user(id) -> User | None:
  return User.get(id)

def load_voting(voting: Voting):
  session["voting"] = voting.id

def get_voting() -> Voting | None:
  voting_id = session.get("voting")
  if not voting_id:
    return None
  return Voting.get(voting_id)
