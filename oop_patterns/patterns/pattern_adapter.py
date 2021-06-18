from abc import ABC, abstractmethod


class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class Mapping(ABC):
    @abstractmethod
    def lighten(self, grid):
        pass


class MappingAdapter(Mapping):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        self.adaptee.grid = grid.copy()
        dim = (len(grid), len(grid[0]))
        self.adaptee.set_dim(dim)
        lights = self._find_coords_of_elem(grid, 1)
        obstacles = self._find_coords_of_elem(grid, -1)
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)

        result_grid = self.adaptee.generate_lights()
        return result_grid

    @staticmethod
    def _find_coords_of_elem(grid_, what_to_find):
        coords = []
        for index_x, line in enumerate(grid_):
            for index_y, elem in enumerate(line):
                if elem == what_to_find:
                    coords.append((index_y, index_x))
        return coords
