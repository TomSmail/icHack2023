from quart import Blueprint, request
from quart import Blueprint, current_app
from app.algorithms.findAdjacentNodes import *
from app.algorithms.lockerSearch import Graph, route_parcel
from random import random
from asyncio import gather
from json import dumps
from datetime import datetime

apibp = Blueprint('api', __name__, url_prefix="/api")
producerbp = Blueprint("producer", __name__, url_prefix="/producer")
distributorbp = Blueprint("distributor", __name__, url_prefix="/distributor")

apibp.register_blueprint(producerbp)
apibp.register_blueprint(distributorbp)

FAIL_PENALTY = 5.00

@apibp.route('/')
async def index():
    return "Hello World", 200, {'X-Header': 'Value'}


# For Amazon
# POST - pull parcel out of locker - move to in transit.
@producerbp.route('/parcel/extract', methods = ["POST"])
async def extractParcelFromLocker():
    parcel_id = request.get_json()["id"]
    await current_app.db.execute("UPDATE TABLE parcel SET inTransit = true WHERE parcelId=$1;", parcel_id)       
    return "{'status': 'Success'}", 200

# POST - set lost and update balance.
# pass in the current locker
@producerbp.route('/parcel/setlost', methods = ["POST"])
async def setParcelAsLost():
    parcel_id = request.get_json()["parcel_id"]
    start_locker_id = request.get_json()["start_locker"]

    await current_app.db.execute("DELETE FROM parcel = true WHERE parcelId=$1;", parcel_id)
    user_id = await current_app.db.fetchrow("SELECT userDoing FROM route JOIN routeEvent ON route.routeId = routeEvent.routeId WHERE route(parcelId)=$1 and routeEvent(currLockerId)=$2;", parcel_id, start_locker_id)["userDoing"]
    await current_app.db.execute("UPDATE distributor SET balance = balance - $1, failedDeliveries = failedDeliveries + 1 WHERE distributorId=$2;", FAIL_PENALTY, user_id)

    return "{'status': 'Success'}", 200

# POST - credit user on arrival at locker
# pass locker in which it got placed.
@producerbp.route('/parcel/deposit', methods = ["POST"])
async def placeParcelOnArrival():
    parcel_id = request.get_json()["id"]
    locker_id = request.get_json()["locker_id"]
    user_id = current_app.db.fetchrow("SELECT userDoing FROM route JOIN routeEvent ON route.routeId = routeEvent.routeId WHERE route(parcelId)=$1 and routeEvent(nextLockerId)=$2;", parcel_id, locker_id)["userDoing"]
    final_dest = current_app.db.fetchrow("SELECT destinationLocker FROM parcel WHERE parcelId=$1", parcel_id)["destinationLocker"]
    current_time = datetime.now()
    await gather(user_id, final_dest)

    await current_app.db.execute("UPDATE parcel SET dateIntoLocker = $1, lockerIn = $2 WHERE parcelId=$3;", current_time, locker_id, parcel_id)

    delivery_prize = random()
    await current_app.db.execute("UPDATE distributor SET balance = balance + $1, succeededDeliveries = succeededDeliveries + 1 WHERE distributorId=$2;", delivery_prize, user_id)

    if (locker_id == final_dest):
        await current_app.db.execute("DELETE FROM parcel = true WHERE parcelId=$1;", parcel_id)

    return "{'status': 'Success'}", 200

# POST - Add a new parcel into the system
@producerbp.route('/parcel/create', method = ["POST"])
async def createNewParcel():
    # Create a new parcel row with the data as provided by the user.

    start_locker_id = request.get()["start_locker"]
    end_locker_id = request.get()["end_locker"]
    current_time = datetime.now()

    g = dbBuildGraph()
    best, path = route_parcel(start_locker_id, end_locker_id, current_time, g)

    parcel_id = await current_app.db.execute("INSERT INTO parcel (dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit) VALUES ($1, $2, $3, $4, $5) RETURNING parcelId AS parcelId", current_time, current_time, start_locker_id, end_locker_id, False)
    route_id = await current_app.db.execute("INSERT INTO route (userDoing, lockerIn, destinationLocker, inTransit) VALUES ($1, $2, $3, $4, $5) RETURNING routeId INTO routeId", current_time, current_time, start_locker_id, end_locker_id, False)

    for (start_id, end_id, dep_time, arr_time, user_id) in path:
        await current_app.db.execute("INSERT INTO routeEvent (leaveTime, arrivalTime, currLockerId, nextLockerId, routeId, parcelId, userDoing) VALUES ($1, $2, $3, $4, $5, $6, $7)", dep_time, arr_time, start_id, end_id, route_id, parcel_id, user_id)

    return "{'deliveryTime': '" + best.strftime("%d/%m/%Y, %H:%M:")+"'}", 200

# GET - Get status of a given parcel
@producerbp.route('/parcel/status', methods = ["GET"])
async def getParcelStatus():
    parcel_id = request.args.get()["id"]
    row_returned = await current_app.db.fetchrow("SELECT inTransit, lockerIn FROM parcel WHERE parcel(parcelId)=$1;", parcel_id)

    response = {}
    if row_returned["inTransit"]:
        response["in_transit"] = True
        response["locker_from"] = row_returned["lockerIn"]
        response["locker_to"] = await current_app.db.fetchrow("SELECT nextLockerId FROM route JOIN routeEvent ON route.routeId = routeEvent.routeId WHERE route(parcelId)=$1 and routeEvent(currLockerId)=$2;", parcel_id, row_returned["lockerIn"])["nextLockerId"]
    else:
        response["in_transit"] = False
        response["locker_in"] = row_returned["lockerIn"]
    
    return dumps(response), 200


async def dbBuildGraph():
    journeyRows = await current_app.db.fetch("SELECT (journeyId, distributorId) FROM journey;")
    journeySegments = []
    for journey in journeyRows:
        journeyPoints = await current_app.db.fetch("SELECT (arrivalTime, latitude, longitude) FROM journeyPoint WHERE journeyId = $1 ORDER BY ordinalNumber;", journey["journeyId"])
        for i,pt in enumerate(journeyPoints[:-1]):
            journeySegments.append(Journey(
                pt["arrivalTime"], journeyPoints[i+1]["arrivalTime"], 
                Point(pt["latitude"], pt["longitude"]),
                Point(journeyPoints[i+1]["latitude"], journeyPoints[i+1]["longitude"]),
                journey["distributorId"]
            ))
    
    lockerRows = await current_app.db.fetchrow("SELECT (latitude, longitude, lockerId) FROM locker;")
    nodes = []
    for row in lockerRows:
        nodes.append(Node(Point(row["latitude"], row["longitude"]), row["lockerId"]))
        
    g = Graph()

    arcs = getArcs(journeySegments, nodes)

    g.build_graph(arcs)

    return g

# GET - estimated delivery time from a given start locker
@producerbp.route('/locker/estimate', method = ["GET"])
async def estimatedDeliveryTime():
    start_locker_id = request.args.get()["start_locker"]
    end_locker_id = request.args.get()["end_locker"]
    current_time = datetime.now()

    g = dbBuildGraph()
    best, path = route_parcel(start_locker_id, end_locker_id, current_time, g)

    return "{'deliveryTime': '" + best.strftime("%d/%m/%Y, %H:%M:")+"'}", 200

# POST - Add a new locker at a given location
@producerbp.route('/locker/create', methods = ["POST"])
async def estimatedDeliveryTime():
    # Add a value to the database for a new locker

    capacity = request.get_json()["capacity"]
    latitude = request.get_json()["latitude"]
    longitude = request.get_json()["longitude"]
    await current_app.db.execute("INSERT INTO locker (capacity, latitude, longitude) VALUES ($1, $2, $3);", capacity, latitude, longitude)
    
    return "{'status': 'Success'}", 200


# For Distribution Front End
# POST - create a user account 
@distributorbp.route('/user/create', methods = ["POST"])
async def createNewUserAccount():
    # create user with the required data
    username = request.get_json()["capacity"]
    pfpUrl = request.get_json()["latitude"]
    await current_app.db.execute("INSERT INTO user (username, pfpUrl) VALUES ($1, $2);", username, pfpUrl)
        
    return "{'status': 'Success'}", 200

# POST - add a journey
@distributorbp.route('/journey/add', methods = ["POST"])
async def addNewJourney():
    distributor_id = request.get_json()["distributor_id"]
    start_time = request.get_json()["start_time"]
    end_time = request.get_json()["end_time"]
    journey_points = request.get_json()["journey_points"]

    journey_id = await current_app.db.execute("INSERT INTO journey(startTime, endTime, distributorId) VALUES ($1, $2, $3) RETURNING journeyId INTO journeyId;", start_time, end_time, distributor_id)

    await gather(*[
        current_app.db.execute("INSERT INTO journeyPoint(latitude, longitude, ordinalNumber, journeyId) VALUES ($1, $2, $3, $4);", point["latitude"], point["longitude"], i, journey_id)
        for i, point in enumerate(journey_points)
    ])        

    return "{'status': 'Success'}", 200

# GET - user's journey and start and end locker locations, and like a way of identifying the parcel.
@distributorbp.route('/route/current', methods = ["GET"])
async def getUsersRoute():

    distributor_id = request.args.get()["distributor_id"]
    start_time = request.args.get()["start_time"]
    end_time = request.args.get()["end_time"]
    journey_points = request.args.get()["journey_points"]

    journey_id = await current_app.db.execute("INSERT INTO journey(startTime, endTime, distributorId) VALUES ($1, $2, $3) RETURNING journeyId INTO journeyId;", start_time, end_time, distributor_id)


    current_app.db.fetchrow("SELECT (journeyId) INTO journeyPoint(latitude, longitude, ordinalNumber, journeyId) VALUES ($1, $2, $3, $4);", point["latitude"], point["longitude"], i, journey_id)

    await gather(*[
        current_app.db.execute("INSERT INTO journeyPoint(latitude, longitude, ordinalNumber, journeyId) VALUES ($1, $2, $3, $4);", point["latitude"], point["longitude"], i, journey_id)
        for i, point in enumerate(journey_points)
    ])        

    return "Hello", 200

# GET - user's balance and PFP
@distributorbp.route('/user/info', method = ["GET"])
async def getUserInfo():
    user_id = request.args.get()["user_id"]

    rowReturned = await current_app.db.fetchrow("SELECT (balance, username, pfpUrl, failedDeliveries, succeededDeliveries) FROM distributor WHERE distributorId=$1;", user_id);
    result = {
        "username" : rowReturned["username"],
        "balance" : rowReturned["balance"],
        "pfpUrl" : rowReturned["pfpUrl"],
        "failedDeliveries" : rowReturned["failedDeliveries"],
        "succeededDeliveries" : rowReturned["succeededDeliveries"] 
    }
    return dumps(result), 200,

# GET - locker locations
@distributorbp.route('/locker/getall', method = ["GET"])
async def getLockerLocations():
    lockerRows = await current_app.db.fetchrow("SELECT (latitude, longitude, lockerId) FROM locker;")
    nodes = []
    for row in lockerRows:
        nodes.append( { "latitude": row["latitude"], "longitude" : row["longitude"], "id": row["lockerId"] })
    
    return dumps({"lockers": nodes}), 200

# GET - username to user id
@distributorbp.route('/locker/getall', methods = ["GET"])
async def usernameToUserId():
    username = request.args.get()["username"]
    rowReturned = await current_app.db.fetchrow("SELECT distributorId FROM distributor WHERE username = $1", username)
    return dumps({"username" : rowReturned["username"]}), 200


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

