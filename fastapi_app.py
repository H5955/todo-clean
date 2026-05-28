from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Database
conn = sqlite3.connect("todo.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    due_date TEXT,
    category TEXT
)
""")

conn.commit()

# Add completed column safely
try:
    cursor.execute(
        "ALTER TABLE todos ADD COLUMN completed INTEGER DEFAULT 0"
    )
    conn.commit()
except:
    pass

# Add due_date column safely
try:
    cursor.execute(
        "ALTER TABLE todos ADD COLUMN due_date TEXT"
    )
    conn.commit()
except:
    pass

# Add category column safely
try:
    cursor.execute(
        "ALTER TABLE todos ADD COLUMN category TEXT"
    )
    conn.commit()
except:
    pass


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    cursor.execute(
        """
        SELECT id,
               task,
               completed,
               due_date,
               category
        FROM todos
        """
    )

    todos = cursor.fetchall()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "todos": todos
        }
    )


# Add Task
@app.post("/add")
async def add(
    task: str = Form(...),
    due_date: str = Form(...),
    category: str = Form(...)
):

    cursor.execute(
        """
        INSERT INTO todos
        (task, due_date, category)
        VALUES (?, ?, ?)
        """,
        (task, due_date, category)
    )

    conn.commit()

    return RedirectResponse(
        "/",
        status_code=303
    )


# Complete Task
@app.get("/complete/{todo_id}")
async def complete(todo_id: int):

    cursor.execute(
        "UPDATE todos SET completed = 1 WHERE id = ?",
        (todo_id,)
    )

    conn.commit()

    return RedirectResponse(
        "/",
        status_code=303
    )


# Delete Task
@app.get("/delete/{todo_id}")
async def delete(todo_id: int):

    cursor.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )

    conn.commit()

    return RedirectResponse(
        "/",
        status_code=303
    )
