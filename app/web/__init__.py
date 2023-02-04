from quart import Blueprint, send_file, current_app

webbp = Blueprint('web', __name__, static_folder='./static')


@webbp.route('/')
async def index():
    return await webbp.send_static_file("index.html")
