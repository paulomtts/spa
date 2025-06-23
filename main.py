import uvicorn
import subprocess
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from templates.base import BaseComponent
from templates.components.table.utils import generate_user_data
from templates.components.counter.component import Counter
from templates.components import TableComponent
from templates.components.flow.component import FlowComponent
from templates.components.flow.utils import generate_flow_data_by_type


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run before the app starts
    print("🚀 Starting FastAPI...")
    try:
        # Try to find npm in PATH
        npm_path = shutil.which("npm")
        if npm_path:
            # Use the found npm path
            subprocess.run([npm_path, "run", "build"], check=True, capture_output=True)
        else:
            # Fallback: use shell=True (works on Windows and Unix)
            subprocess.run("npm run build", shell=True, check=True, capture_output=True)
        print("✅ Assets built successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
    except Exception as e:
        print(f"❌ Error during startup: {e}")

    yield

    # Shutdown: Run when the app shuts down
    print("🛑 Shutting down FastAPI...")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
BaseComponent.set_engine(templates)

state = {"count": 0}


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    # 1. Create component objects
    counter = Counter(count=state["count"])
    data, columns = generate_user_data(15)
    user_table = TableComponent(
        title="User Management",
        columns=columns,
        rows=data,
    )

    # Create flow component using utils
    title, nodes, edges = generate_flow_data_by_type("random")
    flow_data = FlowComponent(
        title=title,
        nodes=nodes,
        edges=edges,
    )

    # 2. Pass component objects to the template
    props = {
        "CounterComponent": counter,
        "UserTableComponent": user_table,
        "FlowComponent": flow_data,
    }
    # 3. Render the template
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "props": props},
    )


@app.post("/increment", response_class=HTMLResponse)
async def increment_counter():
    state["count"] += 1
    counter = Counter(count=state["count"])
    return counter._render()


@app.post("/decrement", response_class=HTMLResponse)
async def decrement_counter():
    state["count"] -= 1
    counter = Counter(count=state["count"])
    return counter._render()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
