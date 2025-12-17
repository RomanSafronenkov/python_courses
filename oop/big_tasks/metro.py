class Vertex:
    N_CREATED = 0  # нужно для визуализации
    
    def __new__(cls, *args, **kwargs):  # нужно для визуализации
        cls.N_CREATED += 1  # нужно для визуализации
        return object.__new__(cls)  # нужно для визуализации
    
    def __repr__(self):  # нужно для визуализации
        return f'Vertex #{self.__id}'  # нужно для визуализации
    
    def __init__(self):
        self.__id = self.N_CREATED  # нужно для визуализации
        self._links = []
        
    @property
    def links(self):
        return self._links
    
    def add_link(self, link):
        # print(f"Link {link} is in links: {link in self._links}")
        if link not in self._links:
            self._links.append(link)


class Link:
    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1
        
        v1.add_link(self)
        v2.add_link(self)
        
    @property
    def v1(self):
        return self._v1
    
    @property
    def v2(self):
        return self._v2
    
    @property
    def dist(self):
        return self._dist
    
    @dist.setter
    def dist(self, value):
        if not (isinstance(value, (int, float)) and value > 0):
            raise ValueError('Расстояние должно быть положительным числом')
        self._dist = value
        
    def __eq__(self, other):
        """
        Проверка связи на равенство
        Связь v1 -> v2 тоже самое, что и v2 -> v1
        """
        if (self.v1 == other.v1 and self.v2 == other.v2) or \
        (self.v1 == other.v2 and self.v2 == other.v1):
            return True
        return False
    
    def __repr__(self):  # нужно для визуализации
        return f"Link between {self._v1} and {self._v2} with distance {self._dist}"  # нужно для визуализации


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []
        
    def add_vertex(self, v):
        if v not in self.vertex:
            self._vertex.append(v)
        
    def add_link(self, link):
        if link not in self._links:
            # если связи нет в списке связей графа, то добавить эту связь (v1->v2 == v2->v1)
            self._links.append(link)
            
            # если вершин из новой связи нет в списке вершин, то добавить их в список
            if link.v1 not in self._vertex:
                self._vertex.append(link.v1)
                
            if link.v2 not in self._vertex:
                self._vertex.append(link.v2)
    
    def find_path(self, v1, v2):
        """
        Алгоритм Дейкстры
        """
        # создадим словарь, который будет содержать в себе расстояния от первой вершины до всех остальных
        distances = {v1: 0}  # помечаем первую вершину растоянием в 0
        
        # создадим словари, в которые будем сохранять кратчайшие пути
        vertex_dict = {v: [v] for v in self._vertex}
        links_dict = {v: [] for v in self._vertex}
        
        # расстояние до всех остальных вершин бесконечность, значит они не посещены
        for vertex in self._vertex:
            if vertex == v1:
                continue
            distances[vertex] = float('inf')
            
        # список непосещенных вершин
        not_visited = list(self._vertex)
        
        # до тех пор пока есть непосещенные вершины
        while not_visited:
            not_visited_distances = {key: value for key, value in distances.items() if key in not_visited}
            
            # ищем ближайшую вершину
            vertex = min(not_visited_distances.items(), key=lambda x: x[1])[0]
            
            # какое расстояние от v1 до текущей вершины
            dist = distances[vertex]
            
            # какие есть соседи у текущей вершины
            neighbors_links = vertex.links
            
            # до какой вершины и какое расстояние
            neighbors = [(l, l.v1, l.dist) if l.v1 != vertex else (l, l.v2, l.dist) for l in neighbors_links]
            neighbors = sorted(neighbors, key=lambda x: x[2])
            
            # пройдемся по всем соседям
            for neighbor_link, neighbor, vertex_to_neighbor_dist in neighbors:
                # какое сейчас расстояние от v1 до этого соседа?
                neighbor_dist = distances[neighbor]
                
                # сравним текущее расстояние с расстоянием от vertex до этой вершины
                if dist + vertex_to_neighbor_dist < neighbor_dist:
                    distances[neighbor] = dist + vertex_to_neighbor_dist  # перезапишем новый кратчайший путь
                    
                    vertex_dict[neighbor] = vertex_dict[vertex] + [neighbor]
                    links_dict[neighbor] = links_dict[vertex] + [neighbor_link]
                    
            # вершина vertex посещена
            del not_visited[not_visited.index(vertex)]
            
        # можно посмотреть кратчайшие пути до всех вершин, а также кратчайшие маршруты
        # return distances, vertex_dict, links_dict
    
        # но вернем интересующий нас путь
        return vertex_dict[v2], links_dict[v2]
    
    
class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self._dist = dist


map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))

map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._links))
print(len(map_metro._vertex))
path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(path[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print(path[1])
print(sum([x.dist for x in path[1]]))  # 7