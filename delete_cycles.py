import copy
from maxflow import find_maxflow

"""
Graph Example: 
[
    'A': {'source': 'A', 'destination': 'B', 'value': 150, 'time': '...'}, 
        {'source': 'A', 'destination': 'D', 'value': 180, 'time': '...'}
    'B': {'source': 'B', 'destination': 'C', 'value': 200, 'time': '...'},
        {'source': 'B', 'destination': 'D', 'value': 140, 'time': '...'}
]
""" 
def delete_cycles(graph, new_edge):
    u = new_edge["source"]
    v = new_edge["destination"]
    S = []
    G = copy.deepcopy(graph)
    
    while True:
        path = find_maxflow(G, u, v)
        if path:
            S.append(path)
            max_path_value = find_max_edge(path)['value']            
            remove_strong_edges(G, max_path_value)
        else:
            break

    if len(S) == 0:
        return graph
    
    min_flow_value = float('inf')
    min_path = None

    for path in S:
        path.append(new_edge)
        path_flow_value = find_max_edge(path)['value'] - find_min_edge(path)['value']
        if path_flow_value < min_flow_value:
            min_flow_value = path_flow_value
            min_path = (path, find_min_edge(path)['value'])
    
    # Subtract minimum value from all edges in the cycle
    min_value = min_path[1]
    for edge in min_path[0]:
        source = edge['source']
        if source in graph:
            for neighbor_edge in graph[source]:
                if (neighbor_edge['destination'] == edge['destination'] and 
                    neighbor_edge['time'] == edge['time']):
                    neighbor_edge['value'] -= min_value
                    break
    
    # Clean up zero-valued edges
    cleanup_zero_edges(graph)
    
    return graph

def cleanup_zero_edges(graph):
    """Remove edges with zero or negative values from the graph"""
    for node in list(graph.keys()):
        if node in graph:  # Check if node still exists
            # Filter out zero or negative value edges
            graph[node] = [edge for edge in graph[node] if edge['value'] > 0]
            
            # Remove nodes that have no outgoing edges
            if not graph[node]:
                # Check if this node has any incoming edges
                has_incoming = False
                for other_node in graph:
                    if other_node != node:
                        for edge in graph[other_node]:
                            if edge['destination'] == node:
                                has_incoming = True
                                break
                        if has_incoming:
                            break
                
                # Only remove if no incoming edges either
                if not has_incoming:
                    del graph[node]

def find_min_edge(path):
    return min(path, key= lambda x: x['value'])

def find_max_edge(path):
    return max(path, key= lambda x: x['value'])

def remove_strong_edges(graph, max_val):
    for node in graph:
        temp_edge_list = []
        for item in graph[node]:
            if item['value'] < max_val:
                temp_edge_list.append(item)
        graph[node] = temp_edge_list