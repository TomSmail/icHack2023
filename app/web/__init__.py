from quart import Blueprint, request, send_file, current_app

webbp = Blueprint('web', __name__, static_folder='./static',
                  static_url_path="")


@webbp.route('/')
async def index():
    return await webbp.send_static_file("index.html")




@webbp.route('/register')
async def rerg():
    return await webbp.send_static_file("register.html")


@webbp.route('/login', methods=["GET", "POST"])
async def logine():
    if request.method == "GET":
        return await webbp.send_static_file("login.html")
    else:
        username = request.form['username']
        pw = request.form['psw']  # lmao
        row = await current_app.db.fetchrow(
            'SELECT distributorId FROM distributor WHERE username = $1', username)
        print(row)
