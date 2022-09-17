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
    added = db.Column(db.DateTime, nullable=False)


class ActiveTask(db.Model):
    __tablename__ = "incomplete_task"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(250), nullable=False)
    started = db.Column(db.DateTime, nullable=False)


class CompletedTask(db.Model):
    __tablename__ = "complete_task"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.DateTime, nullable=False)


# db.create_all()

# Current date
date = datetime.today().strftime("%d/%m/%Y")


@app.route("/")
def home():
    return render_template("index.html", date=date, new_tasks=NewTask.query.all(), active_tasks=ActiveTask.query.all(), completed_tasks=CompletedTask.query.all())


@app.route("/add_new_task", methods=["GET", "POST"])
def add_new_task():
    if request.method == "POST":
        time_stamp = datetime.now()

        task_name = request.form.get("new-task").title()
        task = NewTask(name=task_name, added=time_stamp)
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
    time_stamp = datetime.now()

    new_task = NewTask.query.filter_by(id=task_id).first()
    active_task = ActiveTask(name=new_task.name, started=time_stamp)
    db.session.add(active_task)
    db.session.delete(new_task)
    db.session.commit()

    return redirect("/")


@app.route("/add_to_complete/<int:task_id>")
def add_to_complete(task_id):
    time_stamp = datetime.now()

    active_task = ActiveTask.query.filter_by(id=task_id).first()
    print(active_task.name)
    complete_task = CompletedTask(name=active_task.name, completed=time_stamp)
    db.session.add(complete_task)
    db.session.delete(active_task)
    db.session.commit()

    return redirect("/")


@app.route("/undo_complete_task/<int:task_id>")
def undo_complete_task(task_id):
    time_stamp = datetime.now()

    task = CompletedTask.query.filter_by(id=task_id).first()
    new_task = NewTask(name=task.name, added=time_stamp)
    db.session.add(new_task)
    db.session.delete(task)
    db.session.commit()

    return redirect("/")


@app.route("/delete_complete_task/<int:task_id>")
def delete_complete_task(task_id):
    task = CompletedTask.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run()
