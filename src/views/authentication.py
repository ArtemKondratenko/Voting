from flask import Blueprint, redirect, render_template, request, flash
from src.database import db
from src.models.user import User
from flask_login import login_required, login_user, logout_user, current_user

api = Blueprint(
    'register',__name__)

@api.get("/register")
def get_register():
  return render_template("register.html")

@api.post("/register")
def post_register():
  name = request.form["name"]
  password = request.form["password"]
  user = User(name=name, password=password)
  if User.get_user_by_with_password(name, password):
    flash("Пользователь с заданным именем существует", "error")
    return redirect("/register")
  try:
    user.save()
    login_user(user, remember=True)
    flash("Вы успешно зарегистрировались!", 'success')
    return redirect("/pages/home_user")
  except Exception:
    return "Ошибка регистрации"

@api.get("/pages/home_user")
@login_required
def home_user():
  return render_template("home_user.html")

@api.get("/login")
def get_login():
  return render_template("login.html")

@api.post("/login")
def post_login():
  name = request.form["name"]
  password = request.form["password"]
  user = User.get_user_by_with_password(name, password)
  if not user:
    flash("Введены некорректные данные", "error")
    return redirect("/login")
  login_user(user, remember=True)
  flash("Вы успешно вошли в аккаунт!", "success")
  return redirect("/pages/home_user")

@api.get("/logout")
@login_required
def logout():
  logout_user()
  return redirect("/login")
