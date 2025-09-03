from standard_functions import MaxPriorityQueueCustom

def max_edge_of_neighbors(node, destination):
    """Find the edge with maximum value between node and destination"""
    neighbors = [item for item in node if item['destination'] == destination]
    if not neighbors:
        return None
    max_neighbor = max(neighbors, key=lambda x: x['value'])
    return max_neighbor

def get_unique_neighbors(edges):
    """Get unique destination nodes from edge list"""
    unique = set()
    for item in edges:
        unique.add(item['destination'])
    return list(unique)

def find_maxflow(graph, start_node, end_node):
    """
    Find the maxflow path from start_node to end_node using modified Dijkstra's algorithm
    Returns the path as a list of edges, or empty list if no path exists
    """
    if start_node not in graph or end_node not in graph:
        return []
    
    if start_node == end_node:
        return []  # No self-loops allowed
    
    # Initialize distances and parent tracking
    dist = {node: float('-inf') for node in graph}
    dist[start_node] = float('inf')  
    parent = {node: None for node in graph}
    visited = set()
    
    # Use the fixed priority queue
    mpq = MaxPriorityQueueCustom()
    
    # Add all nodes to priority queue
    for node in graph:
        mpq.push(node, dist[node])
    
    while not mpq.is_empty():
        # Get vertex with maximum distance
        current_vertex = mpq.pop()
        
        if current_vertex in visited:
            continue
            
        visited.add(current_vertex)
        
        # If we reached the end node, we can stop
        if current_vertex == end_node:
            break
        
        # Get all unique neighbors
        if current_vertex not in graph:
            continue
            
        neighbors = get_unique_neighbors(graph[current_vertex])
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue
                
            # Find the maximum-valued edge to this neighbor
            max_edge = max_edge_of_neighbors(graph[current_vertex], neighbor)
            if max_edge is None:
                continue
            
            # Calculate new distance (bottleneck path)
            new_distance = min(dist[current_vertex], max_edge["value"])
            
            # If we found a better path, update
            if new_distance > dist[neighbor]:
                dist[neighbor] = new_distance
                parent[neighbor] = max_edge
                # Update priority queue
                mpq.push(neighbor, new_distance)
    
    # Check if end_node is reachable
    if parent[end_node] is None:
        return []  # No path exists
    
    # Reconstruct path by backtracking
    path_edges = []
    current = end_node
    
    while current != start_node:
        edge = parent[current]
        if edge is None:
            return []  # Path broken
        
        path_edges.insert(0, edge)
        current = edge['source']
    
    return path_edges

def debug_maxflow(graph, start_node, end_node):
    """Debug version that prints intermediate steps"""
    print(f"Finding maxflow path from {start_node} to {end_node}")
    
    if start_node not in graph:
        print(f"Start node {start_node} not in graph")
        return []
    if end_node not in graph:
        print(f"End node {end_node} not in graph")
        return []
    
    path = find_maxflow(graph, start_node, end_node)
    
    if path:
        print(f"Found path with {len(path)} edges:")
        for i, edge in enumerate(path):
            print(f"  {i+1}: {edge['source']} -> {edge['destination']} (value: {edge['value']})")
        min_val = min(edge['value'] for edge in path)
        max_val = max(edge['value'] for edge in path)
        print(f"  Min value: {min_val}, Max value: {max_val}, Flow value: {max_val - min_val}")
    else:
        print("No path found")
    
    return path