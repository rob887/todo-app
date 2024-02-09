from flask import Blueprint, redirect, render_template, url_for, request
from .models import Todo
from . import db
from datetime import datetime

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    # print(todo_list)
    message = request.args.get("message", None)
    return render_template("page1.html", todo_list = todo_list, message = message)

@my_view.route("/add", methods = ["POST"])
def add():
    try:
        task = request.form.get("task")
        new_todo = Todo(task = task)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("my_view.home"))
    except:
        message = "There was an error adding your task. Please try again"
        return redirect(url_for("my_view.home", message=message))


@my_view.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home"))