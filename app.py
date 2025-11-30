# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
from data_handler import add_task, get_all_tasks, update_task_status, delete_task, read_tasks

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devkey'  # not for production

# Ensure tasks.json exists so app behaves predictably
if not os.path.exists("tasks.json"):
    with open("tasks.json", "w", encoding="utf-8") as f:
        f.write("[]")

@app.route("/")
def index():
    """Home page with links."""
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    message = None
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if not title:
            message = "Title is required"
        else:
            try:
                task = add_task(title, description)
                message = f"Task added with ID {task['task_id']}"
                return render_template("add.html", message=message, created=task)
            except Exception as e:
                message = f"Error: {str(e)}"
    return render_template("add.html", message=message)

@app.route("/tasks")
def tasks():
    """Show all tasks - optional filter support via query param ?filter=Pending or Completed"""
    filter_status = request.args.get("filter")
    try:
        tasks = get_all_tasks()
    except Exception as e:
        tasks = []
        error = str(e)
        return render_template("tasks.html", tasks=tasks, error=error)
    if filter_status in ("Pending", "Completed"):
        tasks = [t for t in tasks if t.get("status") == filter_status]
    return render_template("tasks.html", tasks=tasks, filter_status=filter_status)

@app.route("/update", methods=["GET", "POST"])
def update():
    message = None
    task_found = None
    if request.method == "POST":
        # We accept either a direct update request: task_id + fields
        task_id = request.form.get("task_id", "").strip()
        new_description = request.form.get("description", "").strip()
        mark_completed = request.form.get("mark_completed") == "on"
        if not task_id:
            message = "Task ID is required"
        else:
            try:
                updated = update_task_status(task_id, mark_complete=mark_completed, new_description=new_description)
                message = f"Task {task_id} updated."
                task_found = updated
            except KeyError:
                message = "Task not found"
            except Exception as e:
                message = f"Error: {str(e)}"
    return render_template("update.html", message=message, task=task_found)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    message = None
    if request.method == "POST":
        task_id = request.form.get("task_id", "").strip()
        if not task_id:
            message = "Task ID is required"
        else:
            try:
                removed = delete_task(task_id)
                message = f"Task {task_id} deleted."
            except KeyError:
                message = "Task not found"
            except Exception as e:
                message = f"Error: {str(e)}"
    return render_template("delete.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
