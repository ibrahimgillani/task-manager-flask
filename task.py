# task.py
# Task class with basic methods
import uuid

class Task:
    def __init__(self, title, description, status="Pending", task_id=None):
        # If task_id not provided, generate a UUID4 short id
        self.task_id = task_id or str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.status = status

    def mark_completed(self):
        """Mark task as completed."""
        self.status = "Completed"

    def update_description(self, new_desc):
        """Update task description."""
        self.description = new_desc

    def display_task_info(self):
        """Return a dictionary representation for storage/rendering."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

# Demonstration code (can be executed standalone)
if __name__ == "__main__":
    t1 = Task("Buy groceries", "Milk eggs bread")
    t2 = Task("Read book", "Finish chapter 4")
    print(t1.display_task_info())
    t2.mark_completed()
    print(t2.display_task_info())
    t1.update_description("Milk eggs bread and bananas")
    print(t1.display_task_info())
