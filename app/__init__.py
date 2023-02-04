from quart import Quart
import asyncpg
import asyncio
import logging

import toml


from .api import apibp
from .web import webbp

from app.db import Database


app = Quart(__name__)
app.config.from_prefixed_env()
app.config.from_file("../config.toml", toml.load)

app.register_blueprint(apibp, url_prefix="/api",)
app.register_blueprint(webbp, )

app.db = Database(app)


@app.route("/bleh")
async def index():
    print(await app.db.execute("SELECT COUNT(*) FROM mytable"))
