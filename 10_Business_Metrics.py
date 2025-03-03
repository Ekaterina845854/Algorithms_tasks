#Вопросы, почему на графе три независимые компоненты, а не две. Первая и вторая ведь буквально соединены через Д1


def find_independent_components(graph):
    visited = set() 
    components = []

    def dfs(node, component):
        visited.add(node)  
        component.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components



def has_cycles(metrics):
    visited = set()
    stack = set()

    def dfs(metric):
        if metric in stack:
            return True
        if metric in visited:
            return False
        
        visited.add(metric)
        stack.add(metric)
        
        for neighbor in metrics.get(metric, []):
            if dfs(neighbor):
                return True
        
        stack.remove(metric)
        return False

    for key in metrics:
        if dfs(key):
            return True
    return False

def topological_sort(graph):

    def dfs(vertex, visited, stack):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor, visited, stack)
        stack.append(vertex)

    visited = set()
    stack = []
    for vertex in graph:
        if vertex not in visited:
            dfs(vertex, visited, stack)

    return stack[::-1]  

def analyze_metrics(metrics):
    components = find_independent_components(metrics)
    results = []

    for component in components:
        subgraph = {node: metrics.get(node, []) for node in component}
        if has_cycles(subgraph):
            results.append((component, True, None))  
        else:
            order = topological_sort(subgraph)
            results.append((component, False, order)) 
    return results




metrics = {                                           
    "Данные1": ["Метрика1", "Метрика2", "Метрика3"],  
    "Метрика2": ["Метрика1"],                                            
     "Метрика3": ["Метрика4", "Метрика5"],                                          
    "Данные2": ["Метрика6"],                          
    "Метрика6": ["Метрика7"],                         
    "Метрика7": ["Метрика8"],                          
    "Метрика8": ["Метрика6"],                          
}                                                     

result = analyze_metrics(metrics)
print(result)
