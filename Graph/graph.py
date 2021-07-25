import sys
from compares import ComparesInterface
from heap import BinaryHeap

# Entry in table for use in Dijkstra's Algorithm
class DijkstraEntry(ComparesInterface):

    def __init__(self, entry):

        self.key = list(entry.keys())[0]
        self.entry = entry[self.key]

    # For use with the binary heap
    def compare(self, object):
        result = None

        if self.entry["total_distance"] > object.entry["total_distance"]:
            result = 1
        elif self.entry["total_distance"] == object.entry["total_distance"]:
            result = 0
        else:
            result = -1

        return result

    def get_key(self):
        return self.key

"""
Class implementation of a directed graph
1. The graph object has a two-level dictionary structure of:
   graph = { vertex_1 : { adj_vertex : distance, adj_vertex : distance}, 
             vertex_2 : { adj_vertex : distance } }

   where the adjacent vertices is a 1st level key in our graph dictionary
     eg) an 'adj_vertex' could be 'vertex_2' or 'vertex_3'
"""
class Graph:

    BIG_NUMBER = sys.maxsize * 2 + 1

    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex_id):
        if vertex_id in self.graph.keys():
            return False
        else:
            self.graph[vertex_id] = {}
            return True

    def remove_vertex(self, vertex_id):
        if vertex_id in self.graph.keys():
            del self.graph[vertex_id]
            return True
        else:
            return False

    def add_edge(self, vertex_from, vertex_to, weight):
        if vertex_from in self.graph.keys():
            if vertex_to in self.graph[vertex_from].keys():
                return False
            else:
                self.graph[vertex_from][vertex_to] = weight
                return True
        else:
            return False

    def remove_edge(self, vertex_from, vertex_to):
        if vertex_from in self.graph.keys():
            if vertex_to in self.graph[vertex_from].keys():
                del self.graph[vertex_from][vertex_to]
                return True
            else:
                return False
        else:
            return False

    """
    ALGORITHMS - Algorithms associated with graphs
    """

    """
    Prim's Algorithm - Minimum Spanning Tree

    Notes: End of algorithm determination implementations
      1. Determine whether the number of vertices in our MST are
        the same as those in our original graph
      2. Determine whether we can no longer find an unconnected vertex to add
        to our MST
    
    The output is in the form of a symmetric directed graph
    """

    def prim(self):
        
        # Store our minimum spanning tree
        mst_graph = {}

        # Let's use the first vertex in our original graph as the starting point
        first_key = list(self.graph.keys())[0]
        mst_graph[first_key] = {}

        while len(mst_graph.keys()) < len(self.graph.keys()):

            # source = source vertex, dest = destination vertex
            shortest_edge = {"value" : None, "source" : None, "dest" : None}

            for vertex_from in mst_graph.keys():
                for vertex_to in self.graph[vertex_from].keys():
                    if not (vertex_to in mst_graph.keys()):
                        current_edge_value = self.graph[vertex_from][vertex_to]
                        if (shortest_edge["value"] == None) or (current_edge_value < shortest_edge["value"]):
                            shortest_edge["value"] = current_edge_value
                            shortest_edge["source"] = vertex_from
                            shortest_edge["dest"] = vertex_to

            # Add the edge to our MST
            mst_graph[shortest_edge["source"]][shortest_edge["dest"]] = shortest_edge["value"]

            # Reverse connection of vertices (as our output is a symmetric graph)
            # New 1st-level key must be added, since our 'vertex_to' vertex must be unconnected
            mst_graph[shortest_edge["dest"]] = {shortest_edge["source"] : shortest_edge["value"]}
                 
        return mst_graph


    """
    Dijkstra's Algorithm - Shortest path (from a vertex)
    """

    def dijkstra(self, vertex):
        entry_dict = {}

        if vertex in self.graph.keys():

            vertex_heap = BinaryHeap(BinaryHeap.MIN_HEAP)

            """
            Add each vertex and their data (total distance, previous node) as an entry
            to a table. Use both a heap and list -> Heap: For sorting the entries by total distance,
            List: For accessing other entries.
            """
            for i in self.graph.keys():

                # Tabel entry setup
                entry = { i : { "previous" : "", "total_distance" : Graph.BIG_NUMBER} }

                if i == vertex:
                    entry[i]["total_distance"] = 0

                dijkstra_entry = DijkstraEntry(entry)
                vertex_heap.add(dijkstra_entry)
                entry_dict.update(entry)

            """
            The vertex with the smallest total distance will be processed first, then
            removed from the table. This is repeated until there are no more vertices
            in the table.
            """
            while not vertex_heap.is_empty():
                current_vertex = vertex_heap.pop().get_key()

                for i in self.graph[current_vertex].keys():

                    if entry_dict[i]["total_distance"] == Graph.BIG_NUMBER:
                        entry_dict[i]["total_distance"] = entry_dict[current_vertex]["total_distance"] + self.graph[current_vertex][i]
                        entry_dict[i]["previous"] = current_vertex

                    elif (entry_dict[current_vertex]["total_distance"] + self.graph[current_vertex][i] < entry_dict[i]["total_distance"]):
                        entry_dict[i]["total_distance"] = entry_dict[current_vertex]["total_distance"] + self.graph[current_vertex][i]
                        entry_dict[i]["previous"] = current_vertex

                    else:
                        pass

        return entry_dict

    # Return a string of vertices and their edges
    def get_string(self):

        graph_string = ""

        for i in self.graph.keys():
            for j in self.graph[i].keys():
                graph_string += str(i) + "->" + str(j) + ":" + str(self.graph[i][j]) + "\n"

        return graph_string