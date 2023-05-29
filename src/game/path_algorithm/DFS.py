class DFS:
    def __init__(self, grid):
        self.name = "DFS"
        self.grid = grid
        self.spawn = self.grid.spawn
        self.goal = self.grid.goal

        self.open_set = {grid.spawn}
        self.came_from = {grid.spawn: None}
        self.explored = set()

    def reset(self):
        self.open_set = {self.spawn}
        self.came_from = {self.spawn: None}
        self.explored = set()

    def get_neighbors(self, cell):
        # Returns walkable neighbors
        neighbors = []
        print(cell)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cell[0] + dx, cell[1] + dy
            if (
                0 <= nx < self.grid.width
                and 0 <= ny < self.grid.height
                and self.grid.CELL_TYPE[self.grid.grid[ny][nx]]["walkable"]
            ):
                neighbors.append((nx, ny))
        return neighbors

    def algorithm_tick(self):
        if not self.open_set:
            return None, self.explored  # No path found

        # Take the last cell from open_set
        current = self.open_set.pop()
        self.explored.add(current)  # Add current cell to explored set

        if current == self.goal:
            path = []
            while current is not None and current != self.spawn:
                path.append(current)
                current = self.came_from[current]
            path.reverse()
            return path, self.explored

        for neighbor in self.get_neighbors(current):
            if neighbor not in self.explored:
                self.came_from[neighbor] = current

                if neighbor not in self.open_set:
                    self.open_set.add(neighbor)

        return None, self.explored  # Path not yet found

