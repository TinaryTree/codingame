"""Othello"""
import sys
from typing import List, Any

import numpy as np


def op_color(color):
    """
    返回对手的颜色
    :param color:
    :return:
    """
    return 1 - color


def action2point(_action):
    """
    字符转坐标
    :param _action:
    """
    x = int(_action[1])
    y = ord(_action[0]) - ord('a') + 1
    return x, y


class Board:
    """
    棋盘, ('.': empty, '0': black, '1': white)
    """
    cur_color: int
    cur_flips: List[Any]

    def __init__(self, _lines, _actions):
        self.actions = _actions
        _board = np.array(_lines)
        _board[_board == '0'] = 0
        _board[_board == '1'] = 1
        _board = np.insert(_board, 8, [['x'] * 8], 1)
        _board = np.insert(_board, 0, [['x'] * 8], 1)
        _board = np.insert(_board, 8, [['x'] * 10], 0)
        _board = np.insert(_board, 0, [['x'] * 10], 0)
        self._board = _board

    def show(self):
        """
        展示棋盘
        """
        print(self._board, file=sys.stderr, flush=False)

    def get_actions(self, color):
        """
        获取可落子的点
        """
        # 第一步 获取所有对手子周围的空白点
        op_nearly_empty_points = set()
        # 如果落子少于一半的添加策略
        # todo 未来在优化残局策略
        op_points = np.argwhere(self._board == op_color(color))
        print(op_points, file=sys.stderr, flush=False)
        for r, l in op_points:
            print((r, l), file=sys.stderr, flush=False)
            if self._board[r][l] == op_color(color):
                for dx, dy in direction:
                    x, y = r + dy, l + dx
                    if self._board[x][y] == '.':
                        op_nearly_empty_points.add((x, y))
        for point in op_nearly_empty_points:
            if self.reversible(point, color):
                yield point

    def reversible(self, point, color):
        """
        检验当前落子是否合法,如果一个方向上成功就不再计算其他方向
        :param point: (x,y)
        :param color: 1 or 0
        :return: False or True
        """
        x, y = point
        _board = self._board
        _board[x][y] = color
        for xd, yd in direction:
            x, y = point
            x += xd
            y += yd
            if _board[x][y] == op_color(color):
                while True:
                    x += xd
                    y += yd
                    if _board[x][y] != op_color(color):
                        break
                if _board[x][y] == color:
                    return True
                else:
                    continue
            else:
                continue
        return False

    def move(self, point, color):
        """
        落子并翻转
        """
        x, y = point
        self._board[x][y] = color
        flips = []
        for xd, yd in direction:
            x, y = point
            cur_dir = []
            while True:
                x += xd
                y += yd
                if self._board[x][y] == op_color(color):
                    cur_dir.append((x, y))
                else:
                    break
            if self._board[x][y] == color:
                flips += cur_dir
            else:
                continue
        for x, y in flips:
            self._board[x][y] = color
        self.cur_flips = flips
        self.cur_color = color

    def undo(self, point):
        """
        撤回上一步
        """
        x, y = point
        self._board[x][y] = '.'
        for x, y in self.cur_flips:
            self._board[x][y] = op_color(self.cur_color)
        pass


direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
_id = int(input())  # id of your player.
print(_id, file=sys.stderr, flush=True)
board_size = int(input())
# game loop
while True:
    lines = [list(input()) for _ in range(board_size)]  # from top to bottom
    action_count = int(input())  # number of legal actions for this turn.
    actions = [input() for _ in range(action_count)]
    board = Board(lines, actions)
    board.show()
    values = []
    for _ in actions:
        p = action2point(_)
        board.move(p, _id)
        value = list(board.get_actions(op_color(_id))).__len__()
        print((_, value), file=sys.stderr, flush=True)
        board.undo(p)
        values.append(value)
    i = values.index(min(values))
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    print(actions[i])
