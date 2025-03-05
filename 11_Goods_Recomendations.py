"""
Вопросы
- Критерий похожести? Похожими считаются первые соседи? До k-го элемента?
- Критерий сортировки? В реализации за основу взята близость к таргету
"""

from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    recommendations = []

    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    recommendations.append(neighbor)
                    queue.append(neighbor)
    return recommendations

if __name__ == "__main__":

    goods = {
        "Дрель": ["Молоток"],
        "Молоток": ["Дрель", "Пила", "Гвозди"],
        "Пила": ["Молоток", "Нож"],
        "Нож": ["Пила", "Вилка", "Ложка"],
        "Вилка": ["Нож"],
        "Ложка": ["Нож"],
        "Гвозди": ["Молоток", "Булава", "Иглы",
                "Серьги-гвоздики"],
        "Булава": ["Гвозди", "Иглы"],
        "Иглы": ["Булава", "Гвозди"],
        "Серьги-гвоздики": ["Кольца", "Заколка",
                            "Гвозди"],
        "Кольца": ["Серьги-гвоздики"],
        "Заколка": ["Серьги-гвоздики", "Расческа"],
        "Расческа": ["Заколка"],
    }


    recommendations = bfs(goods, "Нож")
    print(recommendations)
