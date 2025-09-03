import heapq
import csv 
"""
Edge structure:

'source' node
'destination' node
'time'
'value'

Graph Structure:

Dictionary of Source Nodes and their forward edges:
[
   'A' : {'source': 'A', 'destination': 'B', 'value': 150, 'time': '...'},
   'B' :  {'source': 'B', 'destination': 'C', 'value': 200, 'time': '...'}
]


"""

class PriorityItem:
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority

    def __lt__(self, other):
        # Defines the comparison logic for a max-heap (higher priority comes first)
        return self.priority > other.priority

class MaxPriorityQueueCustom:
    def __init__(self):
        self._queue = []

    def push(self, item, priority):
        heapq.heappush(self._queue, PriorityItem(item, priority))

    def pop(self):
        if not self.is_empty():
            return heapq.heappop(self._queue).item
        else:
            raise IndexError("pop from an empty priority queue")

    def peek(self):
        if not self.is_empty():
            return self._queue[0].item
        else:
            raise IndexError("peek from an empty priority queue")

    def is_empty(self):
        return len(self._queue) == 0
        

    def size(self):
        return len(self._queue)

def detect_cycle(graph):
    visiting = set()
    visited = set()

    # Check every node in case the graph is not fully connected
    for node in graph:
        if node not in visited:
            if dfs_helper(graph, node, visiting, visited):
                return True
                
    # If we get through all nodes without finding a cycle
    return False

def dfs_helper(graph, node, visiting, visited):
    # Mark the current node as being part of the current path
    visiting.add(node)

    # Get neighbors for the current node
    for edge in graph.get(node, []):
        neighbor = edge['destination'] 

        if neighbor in visiting:
            # We've found a back edge to a node in our current path
            return True

        # If we haven't fully explored this neighbor yet, recurse
        if neighbor not in visited:
            if dfs_helper(graph, neighbor, visiting, visited):
                return True
    
    # We're done exploring from this node. Mark it as fully visited.
    visiting.remove(node)
    visited.add(node)

    # No cycle was found along this path
    return False

def add_edge(graph, edge):
    """
    Adds a directed edge to the graph.

    The graph is an adjacency list represented by a dictionary.
    The edge is a dictionary with 'source', 'destination', 'time', and 'value'.
    """
    # Unpack the information from the edge dictionary
    source_node = edge['source']
    dest_node = edge['destination']
    time = edge['time']
    value = edge['value']

    # Ensure the source and destination nodes exist in the graph
    # If a node isn't in the graph, add it with an empty list of neighbors.
    if source_node not in graph:
        graph[source_node] = []
    if dest_node not in graph:
        graph[dest_node] = []

    # Create the neighbor dictionary to be added to the source node's list
    neighbor_entry = {
        'source': source_node,
        'destination': dest_node,
        'time': time,
        'value': value
    }

    # Add the new transaction to the source node's list of outgoing edges
    graph[source_node].append(neighbor_entry)

def convert_csv_to_edge_list(csv_file_path):
    """
    Reads a CSV file with transaction data and returns a list of dictionaries
    (an edge_list) sorted chronologically by the 'time' column.

    Args:
        csv_file_path (str): The path to the input CSV file.

    Returns:
        list: A list of edge dictionaries, or an empty list if an error occurs.
    """
    edge_list = []
    
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            required_columns = {'source', 'destination', 'value', 'time'}
            if not required_columns.issubset(reader.fieldnames):
                print(f"Error: CSV file must contain columns: {', '.join(required_columns)}")
                return []

            for row in reader:
                try:
                    edge = {
                        'source': row['source'].strip(),
                        'destination': row['destination'].strip(),
                        'value': float(row['value']),
                        'time': row['time'].strip()
                    }
                    edge_list.append(edge)
                except (ValueError, KeyError) as e:
                    print(f"Warning: Skipping row due to error ({e}). Row: {row}")

    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

    # Sort the list chronologically based on the 'time' key before returning
    # This is a critical step for Algorithm 1
    edge_list.sort(key=lambda x: x['time'])
    
    return edge_list