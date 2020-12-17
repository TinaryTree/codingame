"""Othello"""
import copy
import sys
from typing import List, Any

import numpy as np


def op_color(color):
    """
    返回对手的颜色
    :param color:
    :return:
    """
    return str(1 - int(color))


def action2point(_action):
    """
    字符转坐标
    :param _action:
    """
    x = int(_action[1])
    y = ord(_action[0]) - ord('a') + 1
    return x, y


def point2action(point):
    """
    坐标转字符
    :param point:
    :return:
    """
    x, y = point
    strings = 'xabcdefghx'
    return f"{strings[int(y)]}{x}"


class Board:
    """
    棋盘, ('.': empty, '0': black, '1': white)
    """
    cur_color: int
    cur_flips: List[Any]

    def __init__(self, _lines, _actions, color):
        self.steps = []
        self.color = color
        self.actions = _actions
        _board = np.array(_lines)
        _board = np.insert(_board, 8, [['x'] * 8], 1)
        _board = np.insert(_board, 0, [['x'] * 8], 1)
        _board = np.insert(_board, 8, [['x'] * 10], 0)
        _board = np.insert(_board, 0, [['x'] * 10], 0)
        self._board = _board
        self.depth = 0

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
        for r, l in op_points:
            if self._board[r][l] == op_color(color):
                for dx, dy in direction:
                    x, y = r + dy, l + dx
                    if self._board[x][y] == '.':
                        op_nearly_empty_points.add((x, y))
        for point in op_nearly_empty_points:
            if self.reversible(point, color):
                yield point

    def reversible(self, point, color: str):
        """
        检验当前落子是否合法,如果一个方向上成功就不再计算其他方向
        :type color: str
        :param point: (x,y)
        :param color: 1 or 0
        :return: False or True
        """
        x, y = point
        _board = copy.copy(self._board)
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
        self.steps.append(point)

    def undo(self, point):
        """
        撤回上一步
        """
        x, y = point
        self._board[x][y] = '.'
        self.steps.pop(-1)
        for x, y in self.cur_flips:
            self._board[x][y] = op_color(self.cur_color)
        pass

    def alpha_beta(self, max_depth, color, a, b, best_value=-999999):
        """
        a-b剪枝
        :param best_value:
        :param color:
        :param a:
        :param b:
        :param max_depth:最大递归深度
        :return:
        """

        points = list(board.get_actions(color))
        print(('step', self.steps), file=sys.stderr, flush=False)
        print(('ab', (a, b)), file=sys.stderr, flush=False)
        print(points, file=sys.stderr, flush=False)
        if not points:
            if not list(board.get_actions(op_color(color))):
                return None, self.evaluation(color)
            else:
                color = op_color(color)
                _, _value = self.alpha_beta(max_depth, op_color(color), -b, -a)
                return _value * -1
        if self.depth > max_depth:
            best_value = self.evaluation(color) * -1
            print(('达到最大深度', best_value), file=sys.stderr, flush=False)
        else:
            for _p in points:
                self.move(_p, color)
                self.depth += 1
                _, _value = self.alpha_beta(max_depth, op_color(color), -b, -a)
                _value *= -1
                self.depth -= 1
                board.undo(_p)
                print((_p, _value), file=sys.stderr, flush=False)
                if _value >= b:
                    print('剪枝', file=sys.stderr, flush=False)
                    return _p, _value
                if _value > best_value:
                    best_value = _value
                    best_p = _p
                    if _value > a:
                        a = _value
        return best_p, best_value

    def evaluation(self, color):
        """
        局面评估
        :param color:
        :return:
        """
        moves = self.get_actions(color)
        # stable = getstable(board, mycolor)
        # value = mapweightsum(board, mycolor) + 15 * (len(moves) - len(moves_)) + 10 * sum(stable)
        return len(list(moves))


direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
_id = input()  # id of your player.
print(_id, file=sys.stderr, flush=True)
board_size = int(input())
# game loop
while True:
    lines = [list(input()) for _ in range(board_size)]  # from top to bottom
    action_count = int(input())  # number of legal actions for this turn.
    actions = [input() for _ in range(action_count)]
    board = Board(lines, actions, _id)
    board.show()
    # print(list(map(point2action, board.get_actions(_id))), file=sys.stderr, flush=False)

    # values = []
    # for _ in actions:
    #     p = action2point(_)
    #     board.move(p, _id)
    #     value = list(board.get_actions(op_color(_id))).__len__() * -1
    #     print((_, value), file=sys.stderr, flush=True)
    #     board.undo(p)
    #     values.append(value)
    # i = values.index(max(values))
    # print(actions[i])

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    p, value = board.alpha_beta(2, _id, -9999999, 9999999)
    print(('lastvalue', value), file=sys.stderr, flush=True)
    print(point2action(p))
