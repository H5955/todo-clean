from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
            "todos": todos
        }
    )


@app.post("/add")
async def add(task: str = Form(...)):

    cursor.execute(
        "INSERT INTO todos (task) VALUES (?)",
        (task,)
    )

    conn.commit()

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{todo_id}")
async def delete(todo_id: int):

    cursor.execute(
        "DELETE FROM todos WHERE id=?",
        (todo_id,)
    )

    conn.commit()

    return RedirectResponse("/", status_code=303)
