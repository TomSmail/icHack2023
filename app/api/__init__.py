from quart import Blueprint, current_app

apibp = Blueprint('api', __name__)


@apibp.route('/')
async def index():
    row = await current_app.db.fetchrow("SELECT COUNT(*) FROM mytable")
    print(row)
    return "Hello", 200, {'X-Header': 'Value'}


@apibp.route('/parcel/add')
async def add():
    return "Hello", 200, {'X-Header': 'Value'}


# For Amazon
# POST - pull parcel out of locker - move to in transit.
# POST - credit user on arrival at locker / set lost and update balance.
# POST - parcel into the system
# GET - estimated delivery time from a given start locker
# POST - Add a new locker at a given location

# For Distribution Front End
# POST - create a user account
# POST - add a route
# WS - notify them when they need to get it done
# GET - user's route and start and end locker locations, and like a way of identifying the parcel.
# GET - user's balance and PFP
# GET - locker locations

#

# For the backend
# Determine a parcel's route <- Luke
# Set a parcel's route into the database
# set a journey into the database
# set a new lcoker into the database


# point?

# Tasks:
# poll for events - notify them when they need to do it.


# each journey
# For each journey
#   Set of locker points -> start / end
#          -> start time end time
#

# we are gonna generate some points
