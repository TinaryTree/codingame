"""Othello"""
import random
import sys


class Board:
    """
    棋盘,黑棋用 1 表示，白棋用 O 表示，未落子时用 . 表示
    """

    def __init__(self):
        pass

    def load_map(self, lines):
        for


_id = int(input())  # id of your player.
print(_id, file=sys.stderr, flush=True)
board_size = int(input())
print(board_size, file=sys.stderr, flush=True)
# game loop
while True:
    lines = [input() for _ in range(board_size)]
    action_count = int(input())  # number of legal actions for this turn.
    print(action_count, file=sys.stderr, flush=True)
    actions = [input() for i in range(action_count)]
    print(actions, file=sys.stderr, flush=True)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    # a-h1-8
    print(actions[random.randint(0, action_count - 1)])
