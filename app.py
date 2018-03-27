import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database.db')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACKS_MODIFICATIONS"] = False

db = SQLAlchemy(app)
print app.config["SQLALCHEMY_DATABASE_URI"]
class open(db.Model):
    li = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    age = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    rec_li_2 = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    respid = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)

@app.route('/', methods=["GET", "POST"])
def home():
    answers = None
    word= None
    if request.form:
        try:
            word = request.form.get("word")
            answers = open.query.filter(open.li.like('%'+word+'%'))
        except Exception as e:
            print("Failed to search answer")
            print(e)
    else :
        answers = open.query.all()
    return render_template("index.html", answers=answers, word=word)


if __name__ == "__main__":
    app.run(debug=True)
