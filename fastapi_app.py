from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Database setup
conn = sqlite3.connect("todos.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT
)
""")

conn.commit()


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()

    return templates.TemplateResponse(
    "index.html",
    {
        "request": request,
        "todos": todos
    }
)


# Add task
@app.post("/add")
async def add(task: str = Form(...)):

    cursor.execute(
        "INSERT INTO todos (task) VALUES (?)",
        (task,)
    )

    conn.commit()

    return RedirectResponse("/", status_code=303)


# Delete task
@app.get("/delete/{todo_id}")
async def delete(todo_id: int):

    cursor.execute(
        "DELETE FROM todos WHERE id=?",
        (todo_id,)
    )

    conn.commit()

    return RedirectResponse("/", status_code=303)
