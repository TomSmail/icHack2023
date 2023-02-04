from quart import Blueprint, current_app

apibp = Blueprint('api', __name__)


@apibp.route('/')
async def index():
    row = await current_app.db.fetchrow("SELECT COUNT(*) FROM mytable")
    print(row)
    return "Hello", 200, {'X-Header': 'Value'}
