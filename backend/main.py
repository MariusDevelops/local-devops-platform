import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todos")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class Todo(BaseModel):
    title: str
    done: bool = False


def db():
    return psycopg2.connect(DB_URL)


@app.on_event("startup")
def init():
    with db() as c, c.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN DEFAULT FALSE)""")
        cur.execute("ALTER TABLE todos ADD COLUMN IF NOT EXISTS done BOOLEAN DEFAULT FALSE")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos")
def list_todos():
    with db() as c, c.cursor() as cur:
        cur.execute("SELECT id, title, done FROM todos ORDER BY id")
        return [{"id": r[0], "title": r[1], "done": r[2]} for r in cur.fetchall()]


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    with db() as c, c.cursor() as cur:
        cur.execute("SELECT id, title, done FROM todos WHERE id = %s", (todo_id,))
        r = cur.fetchone()
        if not r:
            raise HTTPException(status_code=404, detail="Not found")
        return {"id": r[0], "title": r[1], "done": r[2]}


@app.post("/todos")
def add_todo(todo: Todo):
    with db() as c, c.cursor() as cur:
        cur.execute("INSERT INTO todos (title, done) VALUES (%s, %s) RETURNING id",
                    (todo.title, todo.done))
        return {"id": cur.fetchone()[0], **todo.model_dump()}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    with db() as c, c.cursor() as cur:
        cur.execute("UPDATE todos SET title = %s, done = %s WHERE id = %s",
                    (todo.title, todo.done, todo_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Not found")
        return {"id": todo_id, **todo.model_dump()}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with db() as c, c.cursor() as cur:
        cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Not found")
        return {"deleted": todo_id}