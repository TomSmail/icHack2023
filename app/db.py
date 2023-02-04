

from typing import Optional, Any

from quart import Quart

import asyncpg

import logging


class Database:
    _db = None

    def __init__(self, app: Optional[Quart] = None, **db_args: Any) -> None:
        self._db_args = db_args
        if app:
            self._init_app(app)
            print("inited")

    def _init_app(self, app: Quart):
        self._url = app.config["DB_CONN"]
        app.before_serving(self._before_srv)
        app.after_serving(self._after_srv)

    async def _before_srv(self):
        self._db = await asyncpg.connect(self._url)
        print(await self._db.fetchrow("SELECT * FROM pg_stat_activity"))
        print("connected!")

    def _after_srv(self):
        self._db.close()
        print("db closed")

    def __getattr__(self, name: str) -> Any:
        print("passing...")
        return getattr(self._db, name)
