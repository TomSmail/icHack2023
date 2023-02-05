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
@producerbp.route('/parcel/extract', methods=["POST"])
async def extractParcelFromLocker():
    parcel_id = request.get_json()["id"]
    await current_app.db.execute("UPDATE TABLE parcel SET inTransit = true WHERE parcelId=$1;", parcel_id)
    return "{\"status\": \"success\"}", 200

# POST - set lost and update balance.
# pass in the current locker


@producerbp.route('/parcel/setlost', methods=["POST"])
async def setParcelAsLost():
    parcel_id = request.get_json()["parcel_id"]
    start_locker_id = request.get_json()["start_locker"]

    await current_app.db.execute("DELETE FROM parcel = true WHERE parcelId=$1;", parcel_id)
    user_id = await current_app.db.fetchrow("SELECT userDoing FROM route JOIN routeEvent ON route.routeId = routeEvent.routeId WHERE route(parcelId)=$1 and routeEvent(currLockerId)=$2;", parcel_id, start_locker_id)["userDoing"]
    await current_app.db.execute("UPDATE distributor SET balance = balance - $1, failedDeliveries = failedDeliveries + 1 WHERE distributorId=$2;", FAIL_PENALTY, user_id)

    return "{\"status\": \"success\"}", 200

# POST - credit user on arrival at locker
# pass locker in which it got placed.


@producerbp.route('/parcel/deposit', methods=["POST"])
async def placeParcelOnArrival():
    parcel_id = (await request.get_json())["id"]
    locker_id = (await request.get_json())["locker_id"]
    print(parcel_id)
    print(locker_id)
    user_id = (await current_app.db.fetchrow("SELECT routeEvent.userDoing FROM route JOIN routeEvent ON route.routeId = routeEvent.routeId WHERE route.parcelId=$1 and routeEvent.nextLockerId=$2;", parcel_id, locker_id))["userDoing"]
    final_dest = (await current_app.db.fetchrow("SELECT destinationLocker FROM parcel WHERE parcelId=$1", parcel_id))["destinationLocker"]
    current_time = datetime.now()
    await gather(user_id, final_dest)

    await current_app.db.execute("UPDATE parcel SET dateIntoLocker = $1, lockerIn = $2 WHERE parcelId=$3;", current_time, locker_id, parcel_id)

    delivery_prize = random()
    await current_app.db.execute("UPDATE distributor SET balance = balance + $1, succeededDeliveries = succeededDeliveries + 1 WHERE distributorId=$2;", delivery_prize, user_id)

    if (locker_id == final_dest):
        await current_app.db.execute("DELETE FROM parcel = true WHERE parcelId=$1;", parcel_id)

    return "{'status': 'Success'}", 200

# GET - Get status of a given parcel


@producerbp.route('/parcel/status', methods=["GET"])
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
    today = datetime.today()

    for journey in journeyRows:
        journeyPoints = await current_app.db.fetch("SELECT (arrivalTime, latitude, longitude, journeyPointId) FROM journeyPoint WHERE journeyId = $1 ORDER BY ordinalNumber;", journey["row"][0])
        for i,pt in enumerate(journeyPoints[:-1]):
            journeySegments.append(Journey(
                datetime.combine(today, pt["row"][0]), datetime.combine(today,journeyPoints[i+1]["row"][0]), 
                Point(pt["row"][1], pt["row"][2], pt["row"][3]),
                Point(journeyPoints[i+1]["row"][1], journeyPoints[i+1]["row"][2], pt["row"][3]),
                journey["row"][1]
            ))

    lockerRows = await current_app.db.fetch("SELECT (latitude, longitude, lockerId) FROM locker;")
    nodes = []
    for row in lockerRows:
        nodes.append(Node(Point(row["row"][0], row["row"][1], None), row["row"][2]))
        
    g = Graph()

    arcs = getArcs(journeySegments, nodes)

    g.build_graph(arcs)

    return g



# POST - Add a new locker at a given location


@producerbp.route('/locker/create', methods=["POST"])
async def createLocker():
    # Add a value to the database for a new locker

    capacity = request.get_json()["capacity"]
    latitude = request.get_json()["latitude"]
    longitude = request.get_json()["longitude"]
    await current_app.db.execute("INSERT INTO locker (capacity, latitude, longitude) VALUES ($1, $2, $3);", capacity, latitude, longitude)

    return "{\"status\": \"success\"}", 200




# POST - Add a new parcel into the system


@producerbp.route('/parcel/create', methods=["POST"])
async def createNewParcel():
    # Create a new parcel row with the data as provided by the user.

    start_locker_id = (await request.get_json())["start_locker"]
    end_locker_id = (await request.get_json())["end_locker"]
    current_time = datetime.now()

    g = await dbBuildGraph()
    print("hop edges")
    print(g.edges)

    best, path = route_parcel(start_locker_id, end_locker_id, current_time, g)

    parcel_id = await current_app.db.fetchval("INSERT INTO parcel (dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit) VALUES ($1, $2, $3, $4, $5) RETURNING parcelId", current_time, current_time, start_locker_id, end_locker_id, False)
    route_id = await current_app.db.fetchval("INSERT INTO route (parcelId) VALUES ($1) RETURNING routeId", parcel_id)

    print("hoppp")
    print(path)
    for (start_id, end_id, dep_time, arr_time, user_id, journeyPointStartId, journeyPointEndId) in path:
        await current_app.db.execute("INSERT INTO routeEvent (leaveTime, arrivalTime, currLockerId, nextLockerId, routeId, parcelId, userDoing, journeyPointStartId, journeyPointEndId) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)", dep_time, arr_time, start_id, end_id, route_id, parcel_id, user_id, journeyPointStartId.id, journeyPointEndId.id)

    return "{\"deliveryTime\": \"" + best.strftime("%d/%m/%Y, %H:%M:")+"\"}", 200

# GET - estimated delivery time from a given start locker
@producerbp.route('/locker/estimate', methods = ["GET"])
async def estimatedDeliveryTime():
    start_locker_id = request.args.get("start_locker")
    end_locker_id = request.args.get("end_locker")
    current_time = datetime.now()

    g = await dbBuildGraph()
    print("h2op edges")
    print(g.edges)

    best, path = route_parcel(start_locker_id, end_locker_id, current_time, g)

    return "{\"deliveryTime\": \"" + best.strftime("%d/%m/%Y, %H:%M:")+"\"}", 200


# For Distribution Front End

# GET - user's journey and start and end locker locations, and like a way of identifying the parcel.
# provide route event id
@distributorbp.route('/route_part/get', methods=["GET"])
async def getRoutePart():

    route_part_id = int(request.args.get("route_part_id"))
    print(route_part_id)
    rowReturned = await current_app.db.fetchrow("SELECT (currLockerId, nextLockerId, parcelId, journeyPointStartId, journeyPointEndId) FROM routeEvent WHERE routeEventId = $1;", route_part_id)
    print(rowReturned)

    startLocker = await current_app.db.fetchrow("SELECT (latitude, longitude) FROM locker WHERE lockerId = $1;", rowReturned["row"][0])
    endLocker = await current_app.db.fetchrow("SELECT (latitude, longitude) FROM locker WHERE lockerId = $1;", rowReturned["row"][1])

    startPosn = await current_app.db.fetchrow("SELECT (latitude, longitude) FROM locker WHERE lockerId = $1;", rowReturned["row"][3])
    endPosn = await current_app.db.fetchrow("SELECT (latitude, longitude) FROM locker WHERE lockerId = $1;", rowReturned["row"][4])

# RETURN COORDS.
    result = {
        "startLocker": {
            "lat": startLocker["row"][0],
            "lon": startLocker["row"][1]
        },     
        "endLocker": {
            "lat": endLocker["row"][0],
            "lon": endLocker["row"][1]
        },
        "parcelId": rowReturned["row"][2],
        "startPos": {
            "lat": startPosn["row"][0],
            "lon": startPosn["row"][1]
        },
        "endPos": {
            "lat": endPosn["row"][0],
            "lon": endPosn["row"][1]
        }
    }
    return dumps(result), 200



@distributorbp.route('/user/get_routes', methods=["GET"])
async def getUserRoutes():
    user_id = int(request.cookies.get("userid"))

    rowsReturned = await current_app.db.fetch("SELECT * FROM routeEvent WHERE userDoing=$1;", user_id)

    result = {"routes": [*map(lambda x : x["routeid"], rowsReturned)]}
    return dumps(result), 200



# # POST - create a user account
# @distributorbp.route('/user/create', methods = ["POST"])
# async def createNewUserAccount():
#     # create user with the required data
#     username = request.get_json()["capacity"]
#     pfpUrl = request.get_json()["pfpUrl"]
#     await current_app.db.execute("INSERT INTO user (username, pfpUrl) VALUES ($1, $2);", username, pfpUrl)
        
#     return "{\"status\": \"Success\"}", 200

# POST - add a journey


@distributorbp.route('/journey/add', methods=["POST"])
async def addNewJourney():
    print(await request.get_data())
    distributor_id = int((await request.get_json())["distributor_id"])
    journey_points = (await request.get_json())["journey_points"]

    journey_id = await current_app.db.fetchval("INSERT INTO journey(distributorId) VALUES ($1) RETURNING journeyId;", distributor_id)
    print(journey_id)
    for i, point in enumerate(journey_points):   
        await current_app.db.execute("INSERT INTO journeyPoint(latitude, longitude, ordinalNumber, journeyId, arrivalTime) VALUES ($1, $2, $3, $4, $5);", point["latitude"], point["longitude"], i, journey_id, 
             datetime.strptime(point["arrival_time"], '%Y-%m-%d %H:%M:%S')
       )

    return "{\"status\": \"success\"}", 200

# GET - user's balance and PFP


@distributorbp.route('/user/info', methods=["GET"])
async def getUserInfo():
    # user_id = int(request.args.get("user_id"))
    user_id = int(request.cookies.get("userid"))

 
    rowReturned = await current_app.db.fetchrow("SELECT (balance, username, pfpUrl, failedDeliveries, succeededDeliveries) FROM distributor WHERE distributorId=$1;", user_id)
    print(rowReturned)
    result = {
        "username": rowReturned["row"][1],
        "balance": float(rowReturned["row"][0]),
        "pfpUrl": rowReturned["row"][2],
        "failedDeliveries": rowReturned["row"][3],
        "succeededDeliveries": rowReturned["row"][4]
    }
    return dumps(result), 200,

# GET - locker locations


@distributorbp.route('/locker/getall', methods=["GET"])
async def getLockerLocations():
    lockerRows = await current_app.db.fetch("SELECT (latitude, longitude, lockerId) FROM locker;")
    nodes = []
    for row in lockerRows:
        print(row["row"])
        nodes.append(
            {"latitude": row["row"][0], "longitude": row["row"][1], "id": row["row"][2]})

    return dumps({"lockers": nodes}), 200

# GET - username to user id


@distributorbp.route('/user/getid', methods=["GET"])
async def usernameToUserId():
    username = request.args.get("username")
    rowReturned = await current_app.db.fetchrow("SELECT distributorId FROM distributor WHERE username = $1", username)
    print(rowReturned)
    return dumps({"user_id": rowReturned["distributorid"]}), 200


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
