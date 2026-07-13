from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Data Models ---
class Task(BaseModel):
    title: str
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

# --- In-memory list "database" ---
tasks = []
counter = 1  # Auto-increment ID


# --- 1. Create a new task ---
# POST /todos
@app.post("/todos")
def create_task(task: Task):
    global counter
    new_task = {"id": counter, "title": task.title, "completed": task.completed}
    tasks.append(new_task)
    counter += 1
    return new_task


# --- 2. Get all tasks ---
# GET /todos
@app.get("/todos")
def get_all_tasks():
    return tasks


# --- 3. Get a specific task by ID ---
# GET /todos/{id}
@app.get("/todos/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# --- 4. Update a task ---
# PUT /todos/{id}
@app.put("/todos/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.completed is not None:
                task["completed"] = task_update.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# --- 5. Delete a task ---
# DELETE /todos/{id}
@app.delete("/todos/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return {"message": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")