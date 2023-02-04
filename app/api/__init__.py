from quart import Blueprint, render_template
from quart import Blueprint, current_app

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
    try:
        id = request.get_json()["id"]
        await current_app.db.execute("UPDATE TABLE parcel SET inTransit = true WHERE parcelId=$1;", id)       
        return "{'status': 'Success'}", 200
    except Exception as e:
        print("Failed with: ")
        print(e)
        return "{'status': 'Internal Server Error'}", 500

# POST - set lost and update balance.
@producerbp.route('/parcel/setlost', method = ["POST"])
async def setParcelAsLost():
    try:
        id = request.get_json()["id"]
        locker_id = request.get_json()["locker_id"]
        # delete parcel from the database
        # subtract a penalty from the user's score
        # update number of failures in user
        return "{'status': 'Success'}", 200
    except Exception as e:
        print("Failed with: ")
        print(e)
        return "{'status': 'Internal Server Error'}", 500

    return "Hello", 200, {'X-Header': 'Value'}

# POST - credit user on arrival at locker
# pass locker in which it got placed.
@producerbp.route('/parcel/deposit', method = ["POST"])
async def placeParcelOnArrival():
    try:
        id = request.get_json()["id"]
        locker_id = request.get_json()["locker_id"]
        await current_app.db.execute("UPDATE TABLE parcel SET inTransit = false, lockerIn = $2 WHERE parcelId=$1;", id, locker_id)
        # give the user some money
        # update number of successes in user
        # if it has reached the destination, remove it from the system
        return "{'status': 'Success'}", 200
    except Exception as e:
        print("Failed with: ")
        print(e)
        return "{'status': 'Internal Server Error'}", 500

    return "Hello", 200, {'X-Header': 'Value'}

# POST - Add a new parcel into the system
@producerbp.route('/parcel/create', method = ["POST"])
async def createNewParcel():
    # Create a new parcel row with the data as provided by the user.
    return "Hello", 200, {'X-Header': 'Value'}

# GET - Get status of a given parcel
@producerbp.route('/parcel/status', method = ["GET"])
async def getParcelStatus():
    # return a json formatted expression for the locker at which the parcel is,
    # or "in transit"
    return "Hello", 200, {'X-Header': 'Value'}

# GET - estimated delivery time from a given start locker
@producerbp.route('/locker/estimate', method = ["GET"])
async def estimatedDeliveryTime():
    # call Luke's algorithm
    return "Hello", 200, {'X-Header': 'Value'}

# POST - Add a new locker at a given location
@producerbp.route('/locker/create', method = ["POST"])
async def estimatedDeliveryTime():
    # Add a value to the database for a new locker
    return "Hello", 200, {'X-Header': 'Value'}

# For Distribution Front End
# POST - create a user account 
@distributorbp.route('/user/create', method = ["POST"])
async def createNewUserAccount():
    # create user with the required data
    return "Hello", 200, {'X-Header': 'Value'}

# POST - add a route
@distributorbp.route('/route/add', method = ["POST"])
async def addNewRoute():
    # take the route event data and create routeEvents and routes
    return "Hello", 200, {'X-Header': 'Value'}

# GET - user's route and start and end locker locations, and like a way of identifying the parcel.
@distributorbp.route('/route/current', method = ["GET"])
async def getUsersRoute():
    # GET - user's route and start and end locker locations, and like a way of identifying the parcel.
    return "Hello", 200, {'X-Header': 'Value'}

# GET - user's balance and PFP
@distributorbp.route('/user/info', method = ["GET"])
async def getUserInfo():
    return "Hello", 200, {'X-Header': 'Value'}

# GET - locker locations
@distributorbp.route('/locker/getall', method = ["GET"])
async def getLockerLocations():
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

