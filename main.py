from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class NewTask(db.Model):
    __tablename__ = "new_task"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)


class ActiveTask(db.Model):
    __tablename__ = "incomplete_task"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    started = db.Column(db.String(10), nullable=False)
    completed = db.Column(db.String(10), nullable=False)


class CompleteTask(db.Model):
    __tablename__ = "complete_task"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(250), nullable=False)
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
    return render_template("index.html", date=date, tasks=NewTask.query.all())


@app.route("/add_new_task", methods=["GET", "POST"])
def add_new_task():
    if request.method == "POST":
        task = request.form.get("new-task").title()
        print(task, time, date)
        task = NewTask(name=task, time=time, date=date)
        db.session.add(task)
        db.session.commit()

        return redirect("/")


@app.route("/delete_new_task/<int:task_id>")
def delete_new_task(task_id):
    task = NewTask.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()

    return redirect("/")


@app.route("/add_to_progress/<int:task_id>")
def add_to_progress(task_id):
    task = NewTask.query.filter_by(id=task_id).first()
    task_name = task.name

    print(task.name)

    return redirect("/")


if __name__ == "__main__":
    app.run()
