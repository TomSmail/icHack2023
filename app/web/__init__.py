from quart import Blueprint, make_response, redirect, request, send_file, current_app, url_for

webbp = Blueprint('web', __name__, static_folder='./static',
                  static_url_path="")


@webbp.route('/')
async def index():
    return await webbp.send_static_file("index.html")


@webbp.route('/register')
async def rerg():
    if request.method == "GET":
        return await webbp.send_static_file("register.html")
    elif request.method == "POST":
        username = request.form['username']
        pw = request.form['psw']  # lmao


@webbp.route('/login', methods=["GET", "POST"])
async def logine():
    if request.method == "GET":
        return await webbp.send_static_file("login.html")
    elif request.method == "POST":
        fm = await request.form
        username = fm['username']
        pw = fm['psw']  # lmao

        # row = await current_app.db.fetchrow(
        #    'SELECT distributorId FROM distributor WHERE username = $1', username

        async with current_app.db._pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT distributorId FROM distributor WHERE username = $1', username)
        print(row)
        if row == None:
            resp = await make_response(redirect(url_for("web.rerg")))
            return resp
        resp = await make_response(redirect(url_for("web.index")))
        resp.set_cookie('userid', str(row["distributorid"]))
        return resp
