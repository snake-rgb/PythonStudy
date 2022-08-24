# Класс Solver должен находить оптимальный путь, все пути кроме оптимального, стены.
# Должен получать стартовую позицию, финальную точку, карту для решения.
import time
import json


class Solver:
    def __init__(self, maze_map):
        self.start_pos = Maze.start_pos
        self.end_pos = Maze.end_pos
        self.maze_map = maze_map
        self.zero_matrix_list = []
        self.all_path_list = []
        self.optimal_path_list = []
        self.walls_list = []

    # Create empty list with 0
    def create_path_map(self):
        maze_map = self.maze_map
        for i in range(len(maze_map)):
            self.zero_matrix_list.append([])
            for j in range(len(maze_map[i])):
                self.zero_matrix_list[-1].append(0)
        i, j = self.start_pos
        self.zero_matrix_list[i][j] = 1
        return self.zero_matrix_list

    # Find optimal path step by step
    def make_step(self, step):
        zero_matrix = self.zero_matrix_list
        for i in range(len(zero_matrix)):
            for j in range(len(zero_matrix[i])):
                if zero_matrix[i][j] == step:
                    if i > 0 and zero_matrix[i - 1][j] == 0 and self.maze_map[i - 1][j] == 0:
                        zero_matrix[i - 1][j] = step + 1
                    if j > 0 and zero_matrix[i][j - 1] == 0 and self.maze_map[i][j - 1] == 0:
                        zero_matrix[i][j - 1] = step + 1
                    if i < len(zero_matrix) - 1 and zero_matrix[i + 1][j] == 0 and self.maze_map[i + 1][j] == 0:
                        zero_matrix[i + 1][j] = step + 1
                    if j < len(zero_matrix[i]) - 1 and zero_matrix[i][j + 1] == 0 and self.maze_map[i][j + 1] == 0:
                        zero_matrix[i][j + 1] = step + 1

    # Find right way
    def find_optimal_path(self):
        step = 0
        matrix = self.zero_matrix_list

        while matrix[self.end_pos[0]][self.end_pos[1]] == 0:
            step += 1
            self.make_step(step)
        i, j = self.end_pos
        step = matrix[i][j]
        path_list = [(i, j)]

        while step > 1:
            if i > 0 and matrix[i - 1][j] == step - 1:
                i, j = i - 1, j
                path_list.append((i, j))
                step -= 1
            elif j > 0 and matrix[i][j - 1] == step - 1:
                i, j = i, j - 1
                path_list.append((i, j))
                step -= 1
            elif i < len(matrix) - 1 and matrix[i + 1][j] == step - 1:
                i, j = i + 1, j
                path_list.append((i, j))
                step -= 1
            elif j < len(matrix[i]) - 1 and matrix[i][j + 1] == step - 1:
                i, j = i, j + 1
                path_list.append((i, j))
                step -= 1
        path_list.reverse()
        self.optimal_path_list = path_list
        return path_list

    # Find all walls on map
    def find_walls(self):
        walls_list = []
        for i in range(len(self.maze_map)):
            for j in range(len(self.maze_map[i])):
                if self.maze_map[i][j] == 1:
                    walls_list.append((i, j))
        return walls_list

    # Find all possible not optimal ways
    def find_all_path(self):
        if len(self.optimal_path_list) > 0:
            for i in range(len(self.maze_map)):
                for j in range(len(self.maze_map[i])):
                    if self.maze_map[i][j] == 0:
                        self.all_path_list.append((i, j))
        return sorted(set(self.all_path_list) - set(self.optimal_path_list))


class Player:
    def __init__(self):
        self.start_pos = Maze.start_pos
        self.current_pos = list(Maze.start_pos)
        self.end_pos = Maze.end_pos
        self.steps = 0
        Maze.maze_map[Maze.start_pos[0]][Maze.start_pos[1]] = 5
        self.win_state = False
        self.path = 'rrrddllddrrrrrrrrddddrrrrrrrrddllddddllddrrddrrr'

    # Save current position of player on map, change position of player
    def clean_map(self, save_state):
        pos = list(Maze.optimal_path_list[self.steps])
        Maze.maze_map[pos[0]][pos[1]] = 0
        self.current_pos = list(Maze.optimal_path_list[0])
        if save_state == 's':
            Saver.save(self)
        self.steps = 0
        Maze.maze_map[self.start_pos[0]][self.start_pos[1]] = 5
        if save_state == 's':
            Saver.load(self)
        Maze.__str__(Maze)

    def get_lost_check(self):
        if list(Maze.optimal_path_list[self.steps - 1]) == self.current_pos:
            self.clean_map(
                input('You lost and go back GameOver \nGame was restarted press any key to start or s to save'))
            return False
        return True

    def bounds_check(self, direction):

        if direction == 'l' or direction == 'r':
            if 0 <= self.current_pos[1] < len(Maze.maze_map[0]):
                return True
        elif direction == 'u' or direction == 'd':
            if 0 <= self.current_pos[0] < len(Maze.maze_map):
                return True

        return False

    def wall_check(self):

        wall = tuple(self.current_pos)
        for i in Maze.walls_list:
            if i == wall:
                self.clean_map(
                    input('You hit the wall GameOver \nGame was restarted press any key to start or s to save'))
                return False
        return True

    def try_make_step(self, direction):

        if direction == 'l':
            self.current_pos[1] -= 1
            if self.bounds_check(direction):
                if self.get_lost_check():
                    if self.wall_check():
                        print(self.current_pos)
                        self.move()
        if direction == 'r':
            self.current_pos[1] += 1
            if self.bounds_check(direction):
                if self.get_lost_check():
                    if self.wall_check():
                        print(self.current_pos)
                        self.move()
        if direction == 'd':
            self.current_pos[0] += 1
            if self.bounds_check(direction):
                if self.get_lost_check():
                    if self.wall_check():
                        print(self.current_pos)
                        self.move()

        if direction == 'u':
            self.current_pos[0] -= 1
            if self.bounds_check(direction):
                if self.get_lost_check():
                    if self.wall_check():
                        print(self.current_pos)
                        self.move()

    def move(self):

        if self.current_pos != list(Maze.end_pos):
            print(self.current_pos, list(Maze.end_pos))
            if list(Maze.optimal_path_list[self.steps + 1]) == self.current_pos:
                print('You on right way')
                Maze.maze_map[self.current_pos[0]][self.current_pos[1]] = 5
                pos = list(Maze.optimal_path_list[self.steps])
                Maze.maze_map[pos[0]][pos[1]] = 0
                self.steps += 1
                Maze.__str__(Maze)
            else:
                self.clean_map(
                    input('Not optimal step GameOver \nGame was restarted press any key to start or s to save'))

        else:
            Maze.maze_map[self.end_pos[0]][self.end_pos[1] - 1] = 0
            Maze.maze_map[self.end_pos[0]][self.end_pos[1]] = 5
            Maze.__str__(Maze)
            self.clean_map(input('You WIN \n Choose way again to start \n'))

    def auto_play(self, path):
        for i in path:
            self.try_make_step(i)
            time.sleep(0.1)


# Factory ?
class Maze:
    maze_map = [
        # 1 #2 #3 #4 #5 #6 #7 #8 #9 #10#11#12#13#14#15#16#17#18#19
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],  # 2
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],  # 3
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],  # 4
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],  # 5
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],  # 6
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],  # 7
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],  # 8
        [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 9
        [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 10
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],  # 11
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],  # 12
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],  # 13
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],  # 14
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],  # 15
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],  # 16
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],  # 17
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],  # 18
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],  # 19
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 20
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 21

    ]
    start_pos = (1, 0)
    end_pos = (19, 18)
    all_path_list = []
    optimal_path_list = []
    walls_list = []

    def __str__(self):
        for i in Maze.maze_map:
            print(i)
        return 0


# Должен принимать текущую позицию игрока, количество сделанных шагов и сохранять, загружать сохранения
class Saver:

    def load(player):
        with open("save_data.json", "r") as infile:
            steps = json.load(infile)
            player.steps = steps.pop('steps')
            player.current_pos = list(Maze.optimal_path_list[player.steps])
            Maze.maze_map[player.start_pos[0]][player.start_pos[1]] = 0
            Maze.maze_map[player.current_pos[0]][player.current_pos[1]] = 5

    def save(player):
        with open("save_data.json", "w") as outfile:
            json.dump({'steps': player.steps}, outfile)


class Controller:
    solver = Solver(Maze.maze_map)
    solver.create_path_map()
    Maze.optimal_path_list = solver.find_optimal_path()
    Maze.all_path_list = solver.find_all_path()
    Maze.walls_list = solver.find_walls()
    open('save_data.json', 'a+')
    player = Player()
    if len(open('save_data.json', 'r').readline()) > 0:
        if json.load(open('save_data.json', 'r'))['steps'] > 0:
            if input("Do you want load last game y/n") == 'y':
                Saver.load(player)
            else:
                json.dump({'steps': 0}, open("save_data.json", "w"))
    else:
        json.dump({'steps': 0}, open("save_data.json", "w"))
        Saver.load(player)

    # with open("save_data.json", "r") as save_state:
    #     dict = json.load(save_state)

    Maze.__str__(Maze)
    # player.auto_play(player.path)
    while True:
        player.try_make_step(input("Choose way"))


def main():
    Controller()


if __name__ == '__main__':
    main()
