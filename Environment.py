import numpy as np
import heapq


class Environment:
    def __init__(self, grid):
        self.__grid = np.array(grid)

    def astar(self, start, goal):
        """
        parameters:
            start: tuple(x, y)
            goal: tuple(x, y)
        return: list containing coordinates of the path to the goal with a* algorithm (inverse order)
        """
        if start == goal:
            return [start]

        def heuristic(a, b):
            return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

        neighbors = [
            (-1, 1),
            (-1, -1),
            (1, 1),
            (1, -1),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]
        close_set = set()

        came_from = {}

        gscore = {start: 0}

        fscore = {start: heuristic(start, goal)}

        oheap = []
        heapq.heappush(oheap, (fscore[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]
            if current == goal:
                data = []

                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)

            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + heuristic(current, neighbor)

                if 0 <= neighbor[0] < self.__grid.shape[0]:
                    if 0 <= neighbor[1] < self.__grid.shape[1]:
                        if self.__grid[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        # self.__grid bound y walls
                        continue
                else:
                    # self.__grid bound x walls
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(
                    neighbor, 0
                ):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [
                    i[1] for i in oheap
                ]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        return False

    def astar_multiple(self, start, destinations):
        """
        parameters:
            start: tuple(x, y)
            destinations: list of tuples(x, y)
        return: list containing coordinates of the path to the closest destination with a* algorithm (inverse order)
        """
        paths = []

        sorted_dest = sorted(destinations, key=lambda x: self.get_distance(start, x))

        while sorted_dest:
            dest = sorted_dest.pop(0)

            sorted_dest = sorted(sorted_dest, key=lambda x: self.get_distance(start, x))

            path = self.astar(start, dest)

            if path:
                paths.append(path[::-1])
                start = dest
            else:
                return False

        # return one list instead of list of lists
        paths = [item for sublist in paths for item in sublist]

        return paths

    def get_grid(self):
        return self.__grid

    @staticmethod
    def get_distance(pos1, pos2):
        """
        parameters:
            pos1: tuple(x, y)
            pos2: tuple(x, y)
        return: distance between pos1 and pos2
        """
        return np.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)


