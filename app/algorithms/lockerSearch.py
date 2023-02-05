import dataclasses
import datetime
from collections import defaultdict
import heapq as hp
from findAdjacentNodes import Point

@dataclasses.dataclass
class Edge:
    ### Assume time is in Python time object
    end_id : int
    start_time : datetime.time
    duration: datetime.timedelta
    userResponsible: int
    start_location: Point
    end_location: Point

class Graph:

    MAX_DAYS = 99999999
    def __init__(self):
        self.edges = defaultdict(list)
        self.parents = defaultdict(lambda: (-1,-1,-1,-1))

    def add_edge(self, u, v, start_dt : datetime.time, duration, userResponsible : int, startLocation: Point, endLocation: Point):
        self.edges[u].append(Edge(v, start_dt, duration, userResponsible, startLocation, endLocation))

    def build_graph(self, arcs):

        for arc in arcs:
            print(arc)
            self.add_edge(*arc)


    def find_best(self, start_id, end_id, start_time):
        # TODO - Fix when to start date, at the moment just 04/01/2023 at 9am
        self.parents = defaultdict(lambda: (-1,-1,-1,-1,-1,-1))
        #START_DATE = datetime.datetime(2023, 1,4,9)
        MAX_YEAR = datetime.datetime(year=9999, month=1, day=1)
        best = defaultdict(lambda: MAX_YEAR)
        best[start_id] = start_time
        prioq = []
        hp.heapify(prioq)

        hp.heappush(prioq, (start_time, start_id))

        while len(prioq) > 0:
            cur_time : datetime.datetime
            cur_time, next_node = hp.heappop(prioq)


            if best[next_node] < cur_time:
                continue
                ### Can reach this node sooner from a different node

            for edge in self.edges[next_node]:

                ### We can maybe go to each of these nodes
                ### need to check if this route has already left yet

                if edge.start_time.hour < cur_time.hour:
                    ### Need to wait until the next day
                    next_time = datetime.datetime(year=cur_time.year,month=cur_time.month, day = cur_time.day+1)
                    next_time += datetime.timedelta(hours = edge.start_time.hour, minutes = edge.start_time.minute)
                    earliest_arrival = next_time+edge.duration
                else:
                    #print("HERE IN TIME")
                    next_time = datetime.datetime(year=cur_time.year,month=cur_time.month, day = cur_time.day, hour=edge.start_time.hour, minute = edge.start_time.minute)
                    #print("NEXT TIME", next_time, edge.duration)
                    earliest_arrival = next_time+edge.duration


                if earliest_arrival < best[edge.end_id]:
                    self.parents[edge.end_id] = (next_node, earliest_arrival, next_time, edge.userResponsible, edge.start_location, edge.end_location)
                    best[edge.end_id] = earliest_arrival
                    hp.heappush(prioq, (earliest_arrival, edge.end_id))

        return best[end_id]


    def traceback(self, start_id, end_id):

        route = []
        while end_id != start_id and end_id != -1:
            print(end_id, start_id)
            next_node, arr_time, dep_time, user, startLoc, endLoc = self.parents[end_id]
            if next_node == -1:
                break
            route.append((next_node, end_id, dep_time, arr_time, user, startLoc, endLoc))
            end_id = next_node

        route = list(reversed(route))

        return route




def route_parcel(start_node_id, end_node_id, start_time, g):

    # for (start_id, end_id, stime, duration) in edgeList:
    #     #print(type(stime))
    #     assert type(stime) == datetime.time
    #     assert type(duration) == datetime.timedelta

    #     g.add_edge(start_id, end_id, stime, duration)

    res = g.find_best(start_node_id, end_node_id, start_time)
    path = g.traceback(start_node_id, end_node_id)

    return res, path


if __name__ == "__main__":
    testdate = datetime.datetime(2023, 1, 4, 9, 3, 1)
    print(testdate.strftime("%d/%m/%Y, %H:%M:"))
    #print(route_parcel(0,1, [(0,1, testdate.time(), datetime.timedelta(hours = 2))]))

    tgraph = Graph()



    edge1time = datetime.time(9) ### 9am today
    edge1td = datetime.timedelta(hours=2)

    tgraph.add_edge(1,2, edge1time, edge1td, 1)


    edge2time = datetime.time(23) ### 9pm today
    edge2td = datetime.timedelta(hours=3)

    tgraph.add_edge(2,5, edge2time, edge2td, 2)



    edge3time = datetime.time(10) #10am
    edge3td = datetime.timedelta(hours=1)

    tgraph.add_edge(1,3, edge3time, edge3td, 1)

    edge4time = datetime.time(9)
    edge4td = datetime.timedelta(hours=1)

    tgraph.add_edge(3,4, edge4time, edge4td, 3)


    edge5time = datetime.time(10)
    edge5td = datetime.timedelta(hours=3)

    tgraph.add_edge(1,4, edge5time, edge5td, 3)

    edge6time = datetime.time(14)
    edge6td = datetime.timedelta(hours=3)

    tgraph.add_edge(4,5, edge6time, edge6td, 1)


    print(tgraph.find_best(1, 5, testdate))
    res = tgraph.traceback(1, 5)










