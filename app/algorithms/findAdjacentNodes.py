from geopy import distance
import datetime
# point = someone's possible pickup or dropoff locations
# node = locker
# arc = locker to locker
# (i.e arc = there is a journey from a point close to the start locker 
#                               to an end point close to end locker 
#                               (both the points are on the same journey)))

# returns all edges
def getArcs(journeys, nodes):
    arcs = []
    adjNodesDict = getAdjNodesDict(journeys, nodes)
    for node in nodes:
        arcs.extend(adjNodesDict[node])
    return arcs

# output: dictionary with key node and list of startId, endId, startTime and duration
def getAdjNodesDict(journeys, nodes):
    pointNodesDict = getPointNodesDict(journeys, nodes)
    adjNodesDict = {}
    # goes through each journey each person makes
    for journey in journeys:
        # goes through each locker a person could start at
        for startNode in pointNodesDict[journey.startLocation]:
            startNodeAdjNodes = []
            # goes through each locker a person could go to
            for endNode in pointNodesDict[journey.endLocation]:
                # adds the nodes that are adjacent to the start nodes to a list
                # which is then added to the dictionary later
                assert type(journey.startTime) == datetime.datetime

                startNodeAdjNodes.append([startNode.id, endNode.id, journey.startTime.time(), journey.endTime - journey.startTime])
        adjNodesDict[startNode] = startNodeAdjNodes
    return adjNodesDict

# returns lockers that person could go to at a drop off / pick up location
def getPointNodesDict(journeys, nodes):
    nearByMaxDist = 500
    pointNodesDict = {}
    # goes through each journey each person makes
    for journey in journeys:
        nodesCloseToJourneyStart = []
        nodesCloseToJourneyEnd = []
        # goes through each locker
        for node in nodes:
            # if the locker is nearby to the point, 
            # add it to the list of lockers close to the point
            # which will be added to the dictionary later
            if(nearBy(journey.startLocation, node.location, nearByMaxDist)):
                nodesCloseToJourneyStart.append(node)
            if(nearBy(journey.endLocation, node.location, nearByMaxDist)):
                nodesCloseToJourneyEnd.append(node)
                
        pointNodesDict[journey.startLocation] = nodesCloseToJourneyStart
        pointNodesDict[journey.endLocation] = nodesCloseToJourneyEnd
    return pointNodesDict

def nearBy(p1, p2, dist):
    return distance.distance((p1.lat, p1.long), (p2.lat, p2.long)).meters <= dist


import dataclasses
@dataclasses.dataclass
class Point:
    lat: float
    long: float

@dataclasses.dataclass
class Node:
    location: Point
    id: int

@dataclasses.dataclass
class Journey:
    startTime: datetime.datetime
    endTime: datetime.datetime
    startLocation: Point
    endLocation: Point




t1 = Point(52.1951, 0.1313)
t2 = Point(51.5072, 0.1276)



print(type(datetime.datetime(2023, 1, 4, 12, 2, 1).time()) is datetime.time)

print(nearBy(t1,t2,0)) ### About 75km away as expected



## datetime.time (h,m,s)
## datetime.datetime (yy, m, d) h, m, s t1-t2 timedelta object




