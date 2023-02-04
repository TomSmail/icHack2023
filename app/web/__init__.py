from quart import Blueprint, send_file, current_app

webbp = Blueprint('web', __name__, static_folder='./static',
                  static_url_path="")


@webbp.route('/')
async def index():
    return await webbp.send_static_file("index.html")
