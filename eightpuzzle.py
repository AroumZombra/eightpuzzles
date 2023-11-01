import copy
import time
import heapq


class Puzzle:
    """A sliding-block puzzle."""
  
    def __init__(self, grid):
        """Instances differ by their number configurations."""
        self.grid = copy.deepcopy(grid) # No aliasing!
    
    
    def display(self):
        """Print the puzzle."""
        for row in self.grid:
            for number in row:
                print(number, end="")
            print()
        print()

    def moves(self):
        """Return a list of possible moves given the current configuration."""
        moves = []
        row, col = None, None
        for i in range(len(self.grid)):
            if ' ' in self.grid[i]:
                row, col = i, self.grid[i].index(' ')
                break
        if row > 0:
            moves.append('N')
        if row < len(self.grid) - 1:
            moves.append('S')
        if col > 0:
            moves.append('W')
        if col < len(self.grid[0]) - 1:
            moves.append('E')
        return moves
    
    def neighbor(self, move):
        """Return a Puzzle instance like this one but with one move made."""
        row, col = None, None
        for i in range(len(self.grid)):
            if ' ' in self.grid[i]:
                row, col = i, self.grid[i].index(' ')
                break
        if move == 'N':
            new_row = row - 1
            new_col = col
        elif move == 'S':
            new_row = row + 1
            new_col = col
        elif move == 'W':
            new_row = row
            new_col = col - 1
        elif move == 'E':
            new_row = row
            new_col = col + 1
        else:
            raise ValueError(f"Invalid move: {move}")
        if new_row < 0 or new_row >= len(self.grid) or new_col < 0 or new_col >= len(self.grid[0]):
            return None
        new_grid = copy.deepcopy(self.grid)
        new_grid[row][col], new_grid[new_row][new_col] = new_grid[new_row][new_col], new_grid[row][col]
        return Puzzle(new_grid)

    def h(self, goal):
        """Compute the distance heuristic from this instance to the goal."""
        curr_pos = {}
        goal_pos = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                curr_pos[self.grid[i][j]] = (i, j)
                goal_pos[goal.grid[i][j]] = (i, j)

        distance = 0
        for num in curr_pos:
            row, col = curr_pos[num]
            goal_row, goal_col = goal_pos[num]
            distance += abs(row - goal_row) + abs(col - goal_col)

        return distance

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, puzzle, g_cost, h_cost, parent=None, move=None):
        self.puzzle = puzzle
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.parent = parent
        self.move = move

    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost() < other.f_cost()


class Agent:
    """Knows how to solve a sliding-block puzzle with A* search."""
    
    def astar(self, puzzle, goal):
        """Return a list of moves to get the puzzle to match the goal."""
        # Priority queue and add the initial state
        start = Node(puzzle, 0, puzzle.h(goal), None, None)
        frontier = [start]
        explored = set()
        while frontier:
            current_node = heapq.heappop(frontier)
            current_puzzle = current_node.puzzle
            if current_puzzle.grid == goal.grid:
                
                path = []
                while current_node.parent is not None:
                    path.append(current_node.move)
                    current_node = current_node.parent
                return path[::-1]
            if current_puzzle in explored:
                
                continue
            explored.add(current_puzzle)
            for move in current_puzzle.moves():
                neighbor = current_puzzle.neighbor(move)
                if neighbor is None:
                   # This move is not valid
                    continue
                g_cost = current_node.g_cost + 1
                h_cost = neighbor.h(goal)
                new_node = Node(neighbor, g_cost, h_cost, current_node, move)
                heapq.heappush(frontier, new_node)
        return None


def main():
    """Create a puzzle, solve it with A*, and console-animate."""
    
    puzzle = Puzzle([[1, 2, 5], [4, 8, 7], [3, 6, ' ']])
    puzzle.display()
    
    agent = Agent()
    goal = Puzzle([[' ', 1, 2], [3, 4, 5], [6, 7, 8]])
    path = agent.astar(puzzle, goal)
    
    while path:
        move = path.pop(0)
        puzzle = puzzle.neighbor(move)
        time.sleep(1)
        puzzle.display()


if __name__ == '__main__':
    main()
