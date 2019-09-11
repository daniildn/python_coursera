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


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        #      Ширина        ВЫСОТА
        self.adaptee.set_dim(dim)

        lights = []
        obstacles = []

        for x in range(dim[0]):  # ШИРИНА
            for y in range(dim[1]):  # высота
                if grid[y][x] == 1:
                    lights.append((x, y))
                elif grid[y][x] == -1:
                    obstacles.append((x, y))

        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.grid
