from quart import Quart

from .api import apibp
from .web import webbp


app = Quart(__name__)


app.register_blueprint(apibp, url_prefix="/api",)
app.register_blueprint(webbp, )
