import sys
import datetime as dt
from queue import PriorityQueue

import googlemaps as gm

import Graph as graph
import MST


class Frontier():
    def __init__(self, mstCost, prevCost, seq, vertex, time, eat_lunch =False, eat_dinner = False):
        self.mstCost = mstCost
        self.prevCost = prevCost
        self.seq = seq
        self.cur_vertex = vertex
        self.cur_time = time
        self.eat_lunch = eat_lunch
        self.eat_dinner = eat_dinner

    def __eq__(self,other):
        return self.mstCost + self.prevCost == other.mstCost + other.prevCost

    def __lt__(self,other):
        if(len(self.seq) == len(other.seq)):
            return self.mstCost + self.prevCost > other.mstCost + other.prevCost
        return len(self.seq) < len(other.seq)

# first api key = AIzaSyDRj-IVV1g8aqKOZZiRXyHP4CURyFQg4PQ
# second = AIzaSyD3ed4flml2PsCv0-6hz5lh4svn0YCRiTM
def makeGraph(place_to_place, place_to_rest,places,restaurants,duration):

    # places = ["40.109760744757,-88.227207813792", "310 E Springfield Ave, Champaign, IL",
    #            "406 E Green St, Champaign, IL", "509 E Green St, Champaign, IL",
    #            "1401 W Green St, Urbana, IL", "301 N Neil St, Champaign, IL"]
    #
    # restaurants = ["320 N Chestnut St, Champaign, IL", "60 E Green St, Champaign, IL", "410 E Green St, Champaign, IL", "1214 W University Ave, Urbana, IL"]

    graph_dict = {}
    g = graph.Graph(graph_dict)
    time_dict = {}
    moving_time = {}
    gmaps = gm.Client(key = "AIzaSyDRj-IVV1g8aqKOZZiRXyHP4CURyFQg4PQ")

    for i in range(len(places)):
        g.add_vertex(places[i])
        time_dict[places[i]] = duration[i]

    vertex1 = g.vertices()

    for i in range(len(vertex1)):
        for j in range(i+1, len(vertex1)):
            result = gmaps.directions(vertex1[i], vertex1[j], mode="walking")
            number = result[0]['legs'][0]['duration']['text'].split()
            g.add_edge(vertex1[i], vertex1[j], place_to_place[i][j])
            if(len(number) > 2):
                t = number[0] * 60
                t += number[2]
            else:
                t = number[0]
            moving_time[(vertex1[i], vertex1[j])] = t
    return g, time_dict , restaurants, moving_time

def timeadder(time_to_add, current_time):

    adder = dt.timedelta(hours= 0 , minutes= time_to_add, seconds= 0)

    return current_time + adder

def Astarsearch(graph,startpoint,start_time,time_dict, rest_list, place_to_rest, move_time, ptr_time):
    pq = PriorityQueue()
    n_nodes = len(graph.vertices())
    mstCost = MST.mstCost(graph,[startpoint])
    frontier = Frontier(mstCost, 0.0, [startpoint],startpoint, start_time)
    pq.put(frontier)
    found = False
    sequence = [startpoint]
    while(not found):
        curr = pq.get()
        if(len(curr.seq) == n_nodes and curr.eat_lunch == False and curr.eat_dinner == False):
            sequence = curr.seq
            cost = curr.prevCost + curr.mstCost
            break
        if (len(curr.seq) == n_nodes +2 and curr.eat_lunch == True and curr.eat_dinner == True):
            sequence = curr.seq
            cost = curr.prevCost + curr.mstCost
            # print(sequence)
            # print(cost)
            #print(curr.cur_pathcost)
            break
        if (len(curr.seq) == n_nodes+1 and curr.eat_dinner == True): # ate dinner
            sequence = curr.seq
            cost = curr.prevCost + curr.mstCost
            # print(sequence)
            # print(cost)
            #print(curr.cur_pathcost)
            break
        if (len(curr.seq) == n_nodes+1 and curr.eat_lunch == True):
            sequence = curr.seq
            cost = curr.prevCost + curr.mstCost
            # print(sequence)
            # print(cost)
            #print(curr.cur_pathcost)
            break
        if(curr.cur_time.time() >= dt.datetime.time(dt.datetime(100,1,1,11,00,00)) and curr.cur_time.time() <= dt.datetime.time(dt.datetime(100,1,1,13,00,00)) and not curr.eat_lunch):
            curr.eat_lunch = True
            findrest(rest_list, curr,pq,0,place_to_rest,ptr_time)
            continue
        if(curr.cur_time.time() >= dt.datetime.time(dt.datetime(100,1,1,17,00,00)) and curr.cur_time.time() <= dt.datetime.time(dt.datetime(100,1,1,20,00,00)) and not curr.eat_dinner):
            curr.eat_dinner = True
            findrest(rest_list, curr,pq,1,place_to_rest,ptr_time)
            continue # put restaurant into the frontier and do the other loop.
        adj_edges = graph.get_edges(curr.cur_vertex) # get all the adj edges.
        new_visited = []
        for vertex in curr.seq:
            new_visited.append(vertex)
        for edge in adj_edges:
            cur_visit = []
            for vertex in new_visited:
                cur_visit.append(vertex)
            if edge.dest not in cur_visit:
                cur_visit.append(edge.dest)
                time = timeadder(time_dict[edge.dest] + int(move_time[(curr.cur_vertex,edge.dest)]), curr.cur_time)
                cur_mstCost = MST.mstCost(graph,cur_visit)
                frontier = Frontier(cur_mstCost, curr.prevCost+float(edge.weight), cur_visit, curr.cur_vertex, time, curr.eat_lunch, curr.eat_dinner)
                pq.put(frontier)

    return sequence


def findrest(rest_list, cur,pq, indicator, place_to_rest, ptr_time):
    idx = places.index(cur.cur_vertex)
    min_dist = min(place_to_rest[idx])

    rest_idx = place_to_rest[idx].index(min_dist)
    rest = rest_list[rest_idx]
    # got the closest restaurant
    new_visited = []
    for vertex in cur.seq:
        new_visited.append(vertex)
    new_visited.append(rest)
    new_time = cur.cur_time + dt.timedelta(minutes = ptr_time[idx][rest_idx])
    if(indicator == 1): # dinner
        frontier = Frontier(cur.mstCost, cur.prevCost+min_dist, new_visited, cur.cur_vertex, new_time, cur.eat_lunch, True)
    if(indicator == 0): # lunch
        frontier = Frontier(cur.mstCost, cur.prevCost+min_dist, new_visited, cur.cur_vertex, new_time, True, cur.eat_dinner)
    pq.put(frontier)


if __name__ == '__main__':

    start_coord = sys.argv[1]
    x_coord = sys.argv[2]
    y_coord = sys.argv[3]
    pid = sys.argv[4]
    indicator = sys.argv[5]
    print(start_coord,x_coord,y_coord,pid,indicator)
    # start_coord = "40.109760744757,-88.227207813792"
    # x_coord = "40.109760744757,40.11316009999999,40.11045,40.110092,40.109413,40.118977,40.1174,40.11041,40.110638,40.116649"
    # y_coord = "-88.227207813792,-88.2350479,-88.232892,-88.230866,-88.227169,-88.244272,-88.240637,-88.23896,-88.232483,-88.225388"
    # pid = "1,2,3,4,5,6,7,8,9,10"
    # indicator = "0,0,0,0,0,0,1,1,1,1"

    start_coord_list = start_coord.split(",")
    x_coord_list = x_coord.split(",")
    y_coord_list = y_coord.split(",")
    pid_list = pid.split(",")
    indicator_list = indicator.split(",")
    places = []
    restaurants = []
    start = start_coord_list[0]+","+start_coord_list[1]

    pid = {}
    duration = []
    for i in range(len(x_coord_list)):
        if indicator_list[i] == '0': # things to do
            places.append(x_coord_list[i]+","+y_coord_list[i])
            pid[(x_coord_list[i],y_coord_list[i])] = pid_list[i]
            duration.append(60)
        else:
            restaurants.append(x_coord_list[i]+","+y_coord_list[i])
            pid[(x_coord_list[i], y_coord_list[i])] = pid_list[i]
            duration.append(30)

    # places = ["40.109760744757,-88.227207813792", "310 E Springfield Ave, Champaign, IL",
    #                "406 E Green St, Champaign, IL", "509 E Green St, Champaign, IL",
    #                "1401 W Green St, Urbana, IL", "301 N Neil St, Champaign, IL"]
    #
    # restaurants = ["320 N Chestnut St, Champaign, IL", "60 E Green St, Champaign, IL", "410 E Green St, Champaign, IL", "1214 W University Ave, Urbana, IL"]

    gmaps = gm.Client(key="AIzaSyDRj-IVV1g8aqKOZZiRXyHP4CURyFQg4PQ")
    result = gmaps.distance_matrix(places, restaurants, mode="walking")
    place_to_rest = []
    place_to_rest_time = []
    dist_list = result['rows']
    for li in dist_list:
        rest = []
        time = []
        for dist in li['elements']:
            if(dist['distance']['text'].split(" ")[1] == 'm'):
                rest.append(float(dist['distance']['text'].split(" ")[0])/1000)
                time.append(int(dist['duration']['text'].split(" ")[0]))
            else:
                rest.append(float(dist['distance']['text'].split(" ")[0]))
                time.append(int(dist['duration']['text'].split(" ")[0]))

        place_to_rest.append(rest)
        place_to_rest_time.append(time)

    result_dist = gmaps.distance_matrix(places,places, mode="walking")

    place_to_place = []
    place_to_place_time = []
    dist_list = result_dist['rows']
    for li in dist_list:
        rest = []
        for dist in li['elements']:
            if(dist['distance']['text'].split(" ")[1] == 'm'):
                rest.append(float(dist['distance']['text'].split(" ")[0])/1000)
            else:
                rest.append(float(dist['distance']['text'].split(" ")[0]))
        place_to_place.append(rest)

    g, time_dict, rest_list,move_time = makeGraph(place_to_place, place_to_rest,places,restaurants, duration)
    start_time = dt.datetime(100,1,1,9,00,00)

    result = Astarsearch(g, start, start_time, time_dict,rest_list,place_to_rest, move_time, place_to_rest_time)
    pid_result = []
    for coords in result:
        co=coords.split(',')
        pid_result.append(pid[(co[0],co[1])])
    print(pid_result)