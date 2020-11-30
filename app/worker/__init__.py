import asyncio
import os
from typing import Optional

import faust

_faust_app: Optional[faust.App] = None


def get_faust_app() -> Optional[faust.App]:
    return _faust_app


def set_faust_app_for_worker() -> Optional[faust.App]:
    global _faust_app

    _faust_app = faust.App(
        "worker",
        broker=os.getenv("FAUST_BROKER_URL"),
        store="rocksdb://",
        autodiscover=True,
        origin="app.worker",
    )

    return _faust_app


def set_faust_app_for_api() -> Optional[faust.App]:
    global _faust_app

    # NOTE: the loop argument is needed to ensure that the faust app instance
    # is running in the same event loop as the FastAPI instance.
    _faust_app = faust.App(
        "worker",
        broker=os.getenv("FAUST_BROKER_URL"),
        autodiscover=True,
        origin="app.worker",
        loop=asyncio.get_running_loop(),
        reply_create_topic=True,
    )

    return _faust_app
