from quart import Blueprint, render_template, request

webbp = Blueprint('web', __name__, static_folder='./static',
                  template_folder='./templates')


@webbp.route('/')
async def index():
    return await render_template('main.j2', ip=request.remote_addr)
