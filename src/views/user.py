from flask import Blueprint, redirect, render_template, request, abort
from src.database import db
from src.models.user import User
from src.models.voting import Voting
from src.models.voice import Voice
from flask_login import current_user, login_required
from src import auth

api = Blueprint(
  'user',__name__)

