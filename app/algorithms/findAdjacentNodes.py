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
    # print("dictionaiauguiasgfuisaheifoa")
    # print(adjNodesDict)
    for node in nodes:
        if str(node) in adjNodesDict:
            arcs.extend(adjNodesDict[str(node)])
    return arcs

# output: dictionary with key node and list of startId, endId, startTime and duration
def getAdjNodesDict(journeys, nodes):
    pointNodesDict = getPointNodesDict(journeys, nodes)
    print("pnds")
    print(pointNodesDict)
    print("subpnds")
    adjNodesDict = {}
    # goes through each journey each person makes
    for journey in journeys:
        # goes through each locker a person could start at
        for startNode in pointNodesDict[str(journey.startLocation)]:
            startNodeAdjNodes = []
            # goes through each locker a person could go to
            for endNode in pointNodesDict[str(journey.endLocation)]:
                # adds the nodes that are adjacent to the start nodes to a list
                # which is then added to the dictionary later
                # print(type(journey.startTime))
                assert type(journey.startTime) == datetime.datetime

                startNodeAdjNodes.append([startNode.id, endNode.id, journey.startTime.time(), journey.endTime - journey.startTime, journey.userResponsibleId, journey.startLocation, journey.endLocation])
            adjNodesDict[str(startNode)] = startNodeAdjNodes
        # print(startNodeAdjNodes)
    print("adjjjd")
    print(adjNodesDict)
    return adjNodesDict

# returns lockers that person could go to at a drop off / pick up location
def getPointNodesDict(journeys, nodes):
    nearByMaxDist = 500
    pointNodesDict = {}
    # goes through each journey each person makes
    print("nononononooono")
    print(journeys)
    print(nodes)
    for journey in journeys:
        nodesCloseToJourneyStart = []
        nodesCloseToJourneyEnd = []
        # goes through each locker
        for node in nodes:
            # if the locker is nearby to the point, 
            # add it to the list of lockers close to the point
            # which will be added to the dictionary later
            if(nearBy(journey.startLocation, node.location, nearByMaxDist)):
                # print("start")
                # print(journey)
                nodesCloseToJourneyStart.append(node)
            if(nearBy(journey.endLocation, node.location, nearByMaxDist)):
                # print("end")
                # print(journey)
                nodesCloseToJourneyEnd.append(node)
                
        if str(journey.startLocation) in nodesCloseToJourneyStart:
            pointNodesDict[str(journey.startLocation)] += nodesCloseToJourneyStart
        else:
            pointNodesDict[str(journey.startLocation)] = nodesCloseToJourneyStart

        if str(journey.endLocation) in nodesCloseToJourneyEnd:
            pointNodesDict[str(journey.endLocation)] += nodesCloseToJourneyEnd
        else:
            pointNodesDict[str(journey.endLocation)] = nodesCloseToJourneyEnd

    return pointNodesDict

def nearBy(p1, p2, dist):
    # print(f"Distance {p1.lat} {p2.lat}")
    # print(distance.distance((p1.lat, p1.long), (p2.lat, p2.long)).meters)
    # print(distance.distance((p1.lat, p1.long), (p2.lat, p2.long)).meters <= dist)
    return distance.distance((p1.lat, p1.long), (p2.lat, p2.long)).meters <= dist


import dataclasses
@dataclasses.dataclass
class Point:
    lat: float
    long: float
    id: int
  

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
    userResponsibleId: int


if __name__ == "__main__":
    t1 = Point(52.1951, 0.1313, None)
    t2 = Point(51.5072, 0.1276, None)



    print(type(datetime.datetime(2023, 1, 4, 12, 2, 1).time()) is datetime.time)

    print(nearBy(t1,t2,0)) ### About 75km away as expected



    ## datetime.time (h,m,s)
    ## datetime.datetime (yy, m, d) h, m, s t1-t2 timedelta object




