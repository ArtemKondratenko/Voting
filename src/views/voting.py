from flask import Blueprint, redirect, render_template, request, abort,flash
from src.database import db
from src.models.user import User
from src.models.voting import Voting
from src.models.voice import Voice
from src import auth
from flask_login import  current_user, login_required

api = Blueprint(
  'voting',__name__)


@api.get("/create_vote")
def get_voting():
  return render_template("voting.html")

@api.post("/voting")
@login_required
def post_voting():
  name = request.form["name"]
  description = request.form["description"]
  voting = Voting(name=name, description=description, user_id=current_user.id)
  voting.save()
  auth.load_voting(voting)
  return redirect("/pages/home_user")

@api.get("/all_votes")
def all_votes():
  votings = Voting.get_all()
  current_user_votings = {voting.id: current_user.voice_for(voting.id) for voting in votings} # type: ignore
  return render_template("all_votes.html", votings=votings, current_user_votings=current_user_votings)

@api.post("/vote/<status>")
@login_required
def support_vote(status: str):
    voice_status = status == "yes"
    voting_id = int(request.form["voting"])
    current_user_voting = current_user.voice_for(voting_id) # type: ignore
    if not Voting.get(voting_id):
      flash("Нельзя голосовать по несущетсвующему голосованию", "error")
      return redirect("/all_votes")
    if current_user_voting:
      flash("Вы уже проголосовали!", "error")
      return redirect("/all_votes")
    voice = Voice(voting_id=voting_id, user_id=current_user.id, voice_status=voice_status)
    voice.save()
    flash("Вы успешно проголосовали!", "success")
    return redirect("/all_votes")


