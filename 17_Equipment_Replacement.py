import numpy as np
from collections import deque
from queue import PriorityQueue

cost_matrix = np.array([
    [0, 4000, 5400, 9800, 0], 
    [0, 0, 4300, 6200, 8700],   
    [0, 0, 0, 4800, 7100],     
    [0, 0, 0, 0, 4900],         
    [0, 0, 0, 0, 0]             
])

class Edge:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost

n = 5 
edges = []
gr = [[] for _ in range(n)]

for i in range(n):
    for j in range(n):
        cost = cost_matrix[i][j]
        if cost > 0:  
            edges.append(Edge(i, j, cost))
            gr[i].append(len(edges) - 1) 

distances = [float('inf')] * n
visited = [False] * n
distances[0] = 0  

heap = PriorityQueue()
heap.put((0, 0))  

while not heap.empty():
    current_distance, vertex = heap.get()
    
    if visited[vertex]:
        continue
    visited[vertex] = True  

    for edge_id in gr[vertex]:
        e = edges[edge_id]
        to = e.end
        if distances[to] > distances[vertex] + e.cost:
            distances[to] = distances[vertex] + e.cost
            heap.put((distances[to], to))  

print("Минимальные стоимости замены оборудования:")
for year, cost in zip(range(2025, 2029), distances[1:]):
    print(f"Год {year}: {cost}")

