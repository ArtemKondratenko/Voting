from flask import Flask, redirect
from flask_login import login_required
from src.database import db, create_tables
from src.views.authentication import api as register
from src.views.voting import api as voting
from src.auth import login_manager
from src.views.user import api as user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdb"
app.secret_key = "h3uNFUANxnnxjzgnKAOF399"

app.register_blueprint(register)
app.register_blueprint(voting)
app.register_blueprint(user)
db.init_app(app)
create_tables(app)

login_manager.init_app(app)

@app.get("/")
@login_required
def index():
  return redirect("/all_votes")

if __name__ == '__main__':
  app.run(host="0.0.0.0")
