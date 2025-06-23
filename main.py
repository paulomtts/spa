import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from templates.base import BaseComponent
from templates.components.table.utils import generate_user_data
from templates.components.counter.component import CounterComponent
from templates.components import TableComponent
from templates.components.flow.component import FlowComponent
from templates.components.flow.utils import generate_flow_data_by_type

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
BaseComponent.set_engine(templates)

state = {"count": 0}


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    # 1. Create component objects
    counter = CounterComponent(count=state["count"])
    data, columns = generate_user_data(15)
    user_table = TableComponent(
        title="User Management",
        columns=columns,
        rows=data,
    )
    title, nodes, edges = generate_flow_data_by_type("random")
    flow_data = FlowComponent(
        title=title,
        nodes=nodes,
        edges=edges,
    )

    # 2. Render the template
    props = {
        "CounterComponent": counter,
        "UserTableComponent": user_table,
        "FlowComponent": flow_data,
    }
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "props": props},
    )


@app.post("/increment", response_class=HTMLResponse)
async def increment_counter():
    state["count"] += 1
    counter = CounterComponent(count=state["count"])
    return counter.render()


@app.post("/decrement", response_class=HTMLResponse)
async def decrement_counter():
    state["count"] -= 1
    counter = CounterComponent(count=state["count"])
    return counter.render()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
