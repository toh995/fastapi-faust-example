import asyncio
import importlib

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

import app.worker as worker

fastapi_app = FastAPI()


@fastapi_app.on_event("startup")
async def startup():
    # set up the faust app
    worker.set_faust_app_for_api()

    faust_app = worker.get_faust_app()

    # start the faust app in client mode
    asyncio.create_task(
        faust_app.start_client()
    )

@fastapi_app.on_event("shutdown")
async def shutdown():
    faust_app = worker.get_faust_app()

    # graceful shutdown
    await faust_app.stop()

@fastapi_app.get("/", response_class=HTMLResponse)
async def entrypoint():
    get_current_count_task = importlib.import_module(
        "app.worker.tasks.get_current_count",
    )
    count = await get_current_count_task.agent.ask()

    return f"""
        <h1>Current count: {count}</h1>
        <form method="post" action="/increment">
            <input type="submit" value="Increment!">
        </form>
        """


@fastapi_app.post("/increment", response_class=RedirectResponse)
async def increment():
    increment_task = importlib.import_module(
        "app.worker.tasks.increment",
    )
    await increment_task.agent.ask()

    # redirect the user back to the entrypoint
    return RedirectResponse(
        url=fastapi_app.url_path_for("entrypoint"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


if __name__ == "__main__":
    uvicorn.run("app.api:fastapi_app", host="0.0.0.0", port=8000)
