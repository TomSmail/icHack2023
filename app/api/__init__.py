from quart import Blueprint, render_template

apibp = Blueprint('api', __name__)


@apibp.route('/')
async def index():
    return "Hello", 200, {'X-Header': 'Value'}
