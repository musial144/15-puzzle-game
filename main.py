from Board import Board
import sys

if __name__ == "__main__":
    board = Board(sys.argv[3])

    if sys.argv[1] == 'dfs':
        board.solution(board.dfs([sys.argv[2]]),sys.argv[4],sys.argv[5])
    if sys.argv[1] == 'bfs':
        board.solution(board.bfs([sys.argv[2]]),sys.argv[4],sys.argv[5])
    if sys.argv[1] == 'astr':
        board.solution(board.a_star(sys.argv[2]),sys.argv[4],sys.argv[5])