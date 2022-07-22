import queue
import copy
from threading import main_thread
import time

class Board:

    """ Initializer, load a board and sizes of this board from a file
        and we generate a goal our game """
    def __init__(self, file_name):
        size, board = self.load_board(file_name)

        self.w_size, self.k_size = size
        self.goal = self.gen_goal(self.w_size, self.k_size)
        self.board = board
        self.empty_loc = self.search_empty(self.w_size, self.k_size)

    
    """ We print our board """
    def __repr__(self):
        string = ''
        for i in self.board:
            for j in i:
                if j < 10:
                    string += ' '
                string += '   ' + str(j)
            string += '\n'
        return string


    """ we generate a sorted board as a goal our game """
    def gen_goal(self, w_size, k_size):
        goal = [[0 for x in range(k_size)] for y in range(w_size)]
        i = 1
        for x in range(w_size):
            for y in range(k_size):
                goal[x][y] = i
                i += 1
        goal[w_size-1][k_size-1] = 0
        return goal
    

    """ we load a board and sizes of board  froma  file """
    def load_board(self, file_path):
        with open(file_path) as file:
            size = [int(x) for x in next(file).split()]
            array = []
            for line in file:
                array.append([int(x) for x in line.split()])
        return size, array


    """ We search where is empty block (marked as number 0).
        We will move only this block in a board to solve game"""
    def search_empty(self, w_size, k_size):
        for i in range(w_size):
            for j in range(k_size):
                if self.board[i][j] == 0:
                    return (i, j)
        return Exception("Empty chunk not found")


    """ Change string to list. We need it in dfs and alghoritm, becouse
        we get a sequence of movements as one string from first letters of
        worlds 'UP', 'DOWN', 'RIGHT', 'LEFT'. For example we have sequence
        'DURL' or 'RLUP' """
    def string_to_list(self, string):
        list1=[]
        list1[:0]=string
        return list1


    
    def hamming(self, board, w_size, k_size):
        bad_place = 0
        numer = 1
        for i in range(w_size):
            for j in range(k_size):
                if board[i][j] != 0:
                    if(board[i][j] != numer):  
                        bad_place += 1
                numer += 1
                
        return bad_place


    def manhatan(self, board, w_size, k_size):
        distance = 0
        for i in range(w_size):
            for j in range(k_size):
                if(board[i][j] != 0):
                    x_goal = (board[i][j] - 1) // k_size
                    y_goal = (board[i][j] - 1) % w_size
                    distance += abs(i - x_goal) + abs(j - y_goal)
        return distance


    
    def heurestic(self, board, w_size, k_size, heur_type):
            if (heur_type == "hamm"):
                return self.hamming(board, w_size, k_size)
            if (heur_type == "manh"):
                return self.manhatan(board, w_size, k_size)
            return Exception("wrong heuristics")


    """ We send to output files a game results - path how to move 
        an empty block to win game, the length of this path, number
        of visited and checked paths, max length checked path and time
        how lon game was solved"""
    def solution(self, list, solution_file, stats_file):
        path, path_len, num_visited, num_searched, achiv_deep, end_time = list
        file1 = open(solution_file, 'w+')
        file1.write(str(path_len))
        file1.write('\n')
        file1.write(str(path))
        file1.write('\n')
        file1.close
        file = open(stats_file, 'w+')
        file.write(str(path_len))
        file.write('\n')
        file.write(str(num_visited))
        file.write('\n')
        file.write(str(num_searched))
        file.write('\n')
        file.write(str(achiv_deep))
        file.write('\n')
        file.write(str(end_time))
        file.close()


    """  Solving game by A* algorithm. We have opened paths - which 
         we need to check and closed - which we checked and are wrong.
         We solve this by chosen heuristic - manhatan or hamming"""
    def a_star(self, heur_type):
        open = []
        closed = []
        open.append({"board": self.board
                    , "empty_loc": self.empty_loc
                    , "path": ''
                    , "cost": 0 + self.heurestic(self.board, self.w_size, self.k_size, heur_type)
                    , "heur": self.heurestic(self.board, self.w_size, self.k_size, heur_type)})
        achiv_deep = 0
        start_time = time.time()

        while True:
            if not open:
                Exception("Lista pusta")
                break
            node = open.pop(0)
            board = node["board"]
            empty_loc = node["empty_loc"]
            path = node["path"]

            closed.append(board)

            if len(path) > achiv_deep:
                achiv_deep = len(path)

            if board == self.goal:
                path_len = len(path)
                num_visited = len(open)
                num_searched = len(open) + len(closed)
                achiv_deep = achiv_deep
                end_time = (time.time() - start_time) * 1000
                end_time = round(end_time, 3)

                return [path, path_len, num_visited, num_searched, achiv_deep, end_time]

            neighbours = []
            neighbours.append(self.move_up(copy.deepcopy(board),empty_loc) + ['U'])
            neighbours.append(self.move_right(copy.deepcopy(board),empty_loc) + ['R'])
            neighbours.append(self.move_down(copy.deepcopy(board),empty_loc) + ['D'])
            neighbours.append(self.move_left(copy.deepcopy(board),empty_loc) + ['L'])
            
            for neigh in neighbours:
                if neigh[0] not in closed:
                    neigh_path = path + neigh[2]
                    open.append({"board": neigh[0]
                                , "empty_loc": neigh[1]
                                , "path": neigh_path
                                , "cost": self.heurestic(neigh[0], self.w_size, self.k_size, heur_type)
                                + len(neigh_path)
                                , "heur": self.heurestic(neigh[0], self.w_size, self.k_size, heur_type)})
            open = sorted(open, key=lambda d: (d['cost'], d['heur']))        
            


    def dfs(self, seq_search_str):
        seq_search = self.string_to_list(seq_search_str[0])
        graph = queue.LifoQueue()
        searched = set()
        graph.put({"board": self.board, "empty_loc": self.empty_loc, "path": ''})
        max_deep = 20
        deep = 0
        achiv_deep = 0
        start_time = time.time()

        while not graph.empty():
            node = graph.get()
            #print(str(node))
            board = node["board"]  
            empty_loc = node["empty_loc"]   
            deep = len(node["path"])
            #searched.add(node["path"])
            #print(node["path"])

            if deep > max_deep:
                continue

            if len(node["path"]) > achiv_deep:
                achiv_deep = len(node["path"])

            if board == self.goal:
                path_len = len(node["path"])
                num_visited = len(searched)
                num_searched = len(searched) + graph.qsize()
                achiv_deep = achiv_deep
                end_time = (time.time() - start_time) * 1000
                end_time = round(end_time, 3)

                return [node["path"], path_len, num_visited, num_searched, achiv_deep, end_time]

            
            if deep < 0:
                Exception("UWAGA! Głębokość mniejsza od 0!")
                break

            pos_paths = self.possile_path(board, empty_loc, seq_search, node["path"])

            for pth in pos_paths:
                if pth[0] not in searched:
                    searched.add(pth[0])
                    graph.put(self.move_bfs(board, empty_loc, pth[1], node["path"])[0])


    def possile_path(self, brd, emp_loc, move, path):
        path3 = self.move_dfs(brd, emp_loc, move[3], path)
        path2 = self.move_dfs(brd, emp_loc, move[2], path)
        path1 = self.move_dfs(brd, emp_loc, move[1], path)
        path0 = self.move_dfs(brd, emp_loc, move[0], path)
        paths = []
        if path3 != path:
            paths.append((path3, move[3]))
        if path2 != path:
            paths.append((path2, move[2]))
        if path1 != path:
            paths.append((path1, move[1]))
        if path0 != path:
            paths.append((path0, move[0]))

        return paths


    def move_dfs(self, brd, emp_loc, move, path):
        board = copy.deepcopy(brd)
        empty_loc = emp_loc

        if (move == 'U'):
            board, empty_loc = self.move_up(board, empty_loc)
            if(board != brd):
                path = path + move
        if (move == 'R'):
            board, empty_loc = self.move_right(board, empty_loc)
            if(board != brd):
                path = path + move
        if (move == 'D'):
            board, empty_loc = self.move_down(board, empty_loc)
            if(board != brd):
                path = path + move
        if (move == 'L'):
            board, empty_loc = self.move_left(board, empty_loc)
            if(board != brd):
                path = path + move
        
        return path

    def bfs(self, seq_search_str):
        seq_search = self.string_to_list(seq_search_str[0])
        graph = queue.Queue()
        searched = []
        graph.put({"board": self.board, "empty_loc": self.empty_loc, "path": ''})
        achiv_deep = 0
        start_time = time.time()

        while not graph.empty():
            node = graph.get()
            board = node["board"]
            empty_loc = node["empty_loc"]
            
            if len(node["path"]) > achiv_deep:
                achiv_deep = len(node["path"])

            if board == self.goal:
                path_len = len(node["path"])
                num_visited = len(searched)
                num_searched = len(searched) + graph.qsize()
                achiv_deep = achiv_deep
                end_time = (time.time() - start_time) * 1000
                end_time = round(end_time, 3)

                return [node["path"], path_len, num_visited, num_searched, achiv_deep, end_time]

            if board not in searched:
                searched.append(board)

                graph.put(self.move_bfs(board, empty_loc, seq_search[0], node["path"])[0])
                graph.put(self.move_bfs(board, empty_loc, seq_search[1], node["path"])[0])
                graph.put(self.move_bfs(board, empty_loc, seq_search[2], node["path"])[0])
                graph.put(self.move_bfs(board, empty_loc, seq_search[3], node["path"])[0])


    def move_bfs(self, brd, emp_loc, move, path):
        board = copy.deepcopy(brd)
        empty_loc = emp_loc

        if (move == 'U'):
            board, empty_loc = self.move_up(board, empty_loc)
            return [{"board": board, "empty_loc": empty_loc, "path": path + 'U'}]
        if (move == 'R'):
            board, empty_loc = self.move_right(board, empty_loc)
            return [{"board": board, "empty_loc": empty_loc, "path": path + 'R'}]
        if (move == 'D'):
            board, empty_loc = self.move_down(board, empty_loc)
            return [{"board": board, "empty_loc": empty_loc, "path": path + 'D'}]
        if (move == 'L'):
            board, empty_loc = self.move_left(board, empty_loc)
            return [{"board": board, "empty_loc": empty_loc, "path": path + 'L'}]


    def move_up(self, board, empty):
        if empty[0] > 0:
            tmp = board[empty[0]-1][empty[1]]
            board[empty[0]-1][empty[1]] = 0
            board[empty[0]][empty[1]] = tmp
            empty = (empty[0]-1, empty[1])
        
        return [board, empty]


    def move_right(self, board, empty):
        if empty[1] < (self.k_size - 1):
            tmp = board[empty[0]][empty[1] + 1]
            board[empty[0]][empty[1] + 1] = 0
            board[empty[0]][empty[1]] = tmp
            empty = (empty[0], empty[1] + 1)

        return [board, empty]


    def move_down(self, board, empty):

        if empty[0] < (self.w_size - 1):
            tmp = board[empty[0] + 1][empty[1]]
            board[empty[0] + 1][empty[1]] = 0
            board[empty[0]][empty[1]] = tmp
            empty = (empty[0] + 1, empty[1])
        
        return [board, empty]
    
    def move_left(self, board, empty):

        if empty[1] > 0:
            tmp = board[empty[0]][empty[1] - 1]
            board[empty[0]][empty[1] - 1] = 0
            board[empty[0]][empty[1]] = tmp
            empty = (empty[0], empty[1] - 1)
        
        return [board, empty]