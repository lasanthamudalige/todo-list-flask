from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class new_task(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    task = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)


class incomplete_task(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    task = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    started = db.Column(db.String(10), nullable=False)
    completed = db.Column(db.String(10), nullable=False)


class complete_task(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    task = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    started = db.Column(db.String(10), nullable=False)
    completed = db.Column(db.String(10), nullable=False)


# db.create_all()

# Current date
date = datetime.today().strftime("%d/%m/%Y")
time = datetime.today().strftime("%H:%M:%S")


@app.route("/")
def home():
    tasks = new_task.query.all()

    # print(tasks[-1].name)
    return render_template("index.html", date=date, tasks=new_task.query.all())


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task = request.form.get("new-task")
        print(task, time, date)
        task = new_task(task=task, time=time, date=date)
        db.session.add(task)
        db.session.commit()

        return redirect("/")


@app.route("/add_to_progress", methods=["GET", "POST"])
def add_to_progress():
    if request.method == "POST":
        new_task = request.form.get("new-task")
        print(new_task)

        return redirect("/")


if __name__ == "__main__":
    app.run()
