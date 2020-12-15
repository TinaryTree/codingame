"""Othello"""
import random
import sys

import numpy as np


def op_color(color):
    """
    返回对手的颜色
    :param color:
    :return:
    """
    return 1 - color


class Board:
    """
    棋盘, ('.': empty, '0': black, '1': white)
    """

    def __init__(self, _lines, _actions):
        self.actions = _actions
        _board = np.array(_lines)
        _board = np.insert(_board, 8, [['x'] * 8], 1)
        _board = np.insert(_board, 0, [['x'] * 8], 1)
        _board = np.insert(_board, 8, [['x'] * 10], 0)
        _board = np.insert(_board, 0, [['x'] * 10], 0)
        self._board = _board

    def show(self):
        """
        展示棋盘
        """
        print(self._board, file=sys.stderr, flush=True)

    def get_actions(self, color):
        """
        获取可落子的点
        """
        # 第一步 获取所有对手子周围的空白点
        op_nearly_empty_points = set()
        # 如果落子少于一半的添加策略
        # todo 未来在优化残局策略
        for r in range(board_size):
            for l in range(board_size):
                if self._board[r][l] == op_color(color):
                    for dx, dy in direction:
                        x, y = l + dx, r + dy
                        if self._board[x][y] == '.':
                            op_nearly_empty_points.add((x, y))
        for point in op_nearly_empty_points:
            if self.reversible(point, color):
                yield point

    def reversible(self, point, color):
        """
        检验当前落子是否合法,如果一个方向上成功就不在计算其他方向
        :param point: (x,y)
        :param color: 1 or 0
        :return: False or True
        """
        x, y = point
        self._board[x][y] = color
        for xd, yd in direction:
            while True:
                x += xd
                y += yd
                if self._board[x][y] != op_color(color):
                    break
            if self._board == color:
                return True
            else:
                continue
        return False

    def move(self):
        """
        落子并翻转
        """

        pass


direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
_id = int(input())  # id of your player.
print(_id, file=sys.stderr, flush=True)
board_size = int(input())
print(board_size, file=sys.stderr, flush=True)
# game loop
while True:
    lines = [list(input()) for _ in range(board_size)]  # from top to bottom
    action_count = int(input())  # number of legal actions for this turn.
    actions = [input() for _ in range(action_count)]
    board = Board(lines, actions)
    board.show()
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    print(actions[random.randint(0, action_count - 1)])
