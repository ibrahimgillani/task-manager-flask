# data_handler.py
# Functions to read/write tasks.json and perform CRUD operations.
import json
import os
from task import Task

TASKS_FILE = "tasks.json"

def read_tasks():
    """Read tasks from tasks.json, return list of dicts."""
    if not os.path.exists(TASKS_FILE):
        # File missing; return empty list (caller may choose to create file)
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                # Invalid structure
                raise ValueError("Invalid JSON structure: expected list at top level")
            return data
    except json.JSONDecodeError as e:
        # Invalid JSON structure
        raise ValueError("Invalid JSON file: could not decode") from e

def write_tasks(tasks_list):
    """Write list of dict tasks to tasks.json."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_list, f, indent=4)

def add_task(title, description):
    """Create Task object and save to file. Returns created task dict."""
    task = Task(title=title, description=description)
    tasks = read_tasks()
    tasks.append(task.display_task_info())
    write_tasks(tasks)
    return task.display_task_info()

def get_all_tasks():
    return read_tasks()

def find_task_index(task_id):
    tasks = read_tasks()
    for idx, t in enumerate(tasks):
        if t.get("task_id") == task_id:
            return idx
    return None

def update_task_status(task_id, mark_complete=False, new_description=None):
    tasks = read_tasks()
    idx = find_task_index(task_id)
    if idx is None:
        raise KeyError("Task not found")
    # Update using Task class methods for clarity
    tdict = tasks[idx]
    task = Task(
        title=tdict.get("title"),
        description=tdict.get("description"),
        status=tdict.get("status"),
        task_id=tdict.get("task_id")
    )
    if new_description is not None and new_description.strip() != "":
        task.update_description(new_description)
    if mark_complete:
        task.mark_completed()
    tasks[idx] = task.display_task_info()
    write_tasks(tasks)
    return tasks[idx]

def delete_task(task_id):
    tasks = read_tasks()
    idx = find_task_index(task_id)
    if idx is None:
        raise KeyError("Task not found")
    removed = tasks.pop(idx)
    write_tasks(tasks)
    return removed
