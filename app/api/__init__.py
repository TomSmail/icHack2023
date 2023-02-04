from quart import Blueprint, render_template

apibp = Blueprint('api', __name__, url_prefix="/api")
producerbp = Blueprint("producer", __name__, url_prefix="/producer")
distributorbp = Blueprint("distributor", __name__, url_prefix="/distributor")

apibp.register_blueprint(producerbp)
apibp.register_blueprint(distributorbp)


@apibp.route('/')
async def index():
    return "Hello", 200, {'X-Header': 'Value'}


# For Amazon
# POST - pull parcel out of locker - move to in transit.
@producerbp.route('/parcel/extract', method = ["POST"])
async def extractParcelFromLocker():
    return "Hello", 200, {'X-Header': 'Value'}

# POST - credit user on arrival at locker / set lost and update balance.
# Destination = DONE
@producerbp.route('/parcel/deposit', method = ["POST"])
async def placeParcelOnArrival():
    return "Hello", 200, {'X-Header': 'Value'}

# POST - Add a new parcel into the system
@producerbp.route('/parcel/create', method = ["POST"])
async def createNewParcel():
    return "Hello", 200, {'X-Header': 'Value'}

# GET - estimated delivery time from a given start locker
@producerbp.route('/locker/estimate', method = ["GET"])
async def estimatedDeliveryTime():
    return "Hello", 200, {'X-Header': 'Value'}

# POST - Add a new locker at a given location
@producerbp.route('/locker/create', method = ["POST"])
async def estimatedDeliveryTime():
    return "Hello", 200, {'X-Header': 'Value'}

# For Distribution Front End
# POST - create a user account 
@distributorbp.route('/user/create', method = ["POST"])
async def createNewUserAccount():
    return "Hello", 200, {'X-Header': 'Value'}

# POST - add a route
@distributorbp.route('/route/add', method = ["POST"])
async def addNewRoute():
    return "Hello", 200, {'X-Header': 'Value'}

# GET - user's route and start and end locker locations, and like a way of identifying the parcel.
@distributorbp.route('/route/current', method = ["GET"])
async def addNewRoute():
    return "Hello", 200, {'X-Header': 'Value'}

# GET - user's balance and PFP
@distributorbp.route('/user/info', method = ["GET"])
async def addNewRoute():
    return "Hello", 200, {'X-Header': 'Value'}

# GET - locker locations
@distributorbp.route('/locker/getall', method = ["GET"])
async def addNewRoute():
    return "Hello", 200, {'X-Header': 'Value'}


# For the backend
# Determine a parcel's route <- Luke
# Set a parcel's route into the database
# set a journey into the database
# set a new lcoker into the database

# WS - notify them when they need to get it done


# point?

# Tasks:
# poll for events - notify them when they need to do it.

# each journey
# For each journey
#   Set of locker points -> start / end
#          -> start time end time
# 

# we are gonna generate some points

