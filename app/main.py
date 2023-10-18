from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
)
import uvicorn

from db.tools import SqliteTools
from models.models import TodoModel

app = FastAPI()

@app.get("/todo/{todo_id}/")
async def get_todo_by_id(todo_id: int):
    todo = SqliteTools.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo

@app.post("/todo/")
async def create_todo(todo_data: TodoModel):
    todo = SqliteTools.add_todo(todo_data.title, todo_data.description)
    return todo

@app.put("/todo/{todo_id}/")
async def update_todo_by_id(todo_id: int, todo_data: TodoModel):
    todo = SqliteTools.update_todo_by_id(
        todo_id, todo_data.title, todo_data.description, todo_data.completed
    )
    return todo

@app.delete("/todo/{todo_id}/")
async def delete_todo_by_id(todo_id: int):
    deleted = SqliteTools.delete_todo_by_id(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    SqliteTools.check_exists_db()
    uvicorn.run(
        app="main:app", host="127.0.0.1", port=8000, workers=3, reload=True
    )