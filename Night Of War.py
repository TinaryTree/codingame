# Jrke's special
# -Kill your enemy soldiers or Have more bucks than your enemy at end of game
import copy
from typing import List, Tuple

my_id = int(input())  # Your unique player Id
map_size = int(input())  # the size of map MapSize*MapSize

directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


class Soldier:
    def __init__(self, owner_id, x, y, soldier_id, level, direction):
        self.direction = direction
        self.level = level
        self.soldier_id = soldier_id
        self.y = y
        self.x = x
        self.owner_id = owner_id

    def cam_move(self, soldiers, war_map):
        res = []
        if war_map.check(self.x, self.y - 1, soldiers) and self.direction != 2:
            res.append('UP')
        if war_map.check(self.x - 1, self.y, soldiers) and self.direction != 3:
            res.append('LEFT')
        if war_map.check(self.x, self.y + 1, soldiers) and self.direction != 0:
            res.append('DOWN')
        if war_map.check(self.x + 1, self.y, soldiers) and self.direction != 1:
            res.append('RIGHT')
        return res

    def around_pos(self, war_map):
        positions = ((self.x + _x, self.y + _y) for _x, _y in directions)
        positions = ((_x, _y) for _x, _y in positions if war_map.check(_x, _y, my_soldiers))
        if self.direction == 0:  # up
            return [(_x, _y) for _x, _y in positions if _y <= self.y]
        if self.direction == 1:  # LEFT
            return [(_x, _y) for _x, _y in positions if _x <= self.x]
        if self.direction == 2:  # DOWN
            return [(_x, _y) for _x, _y in positions if _y >= self.y]
        if self.direction == 3:  # RIGHT
            return [(_x, _y) for _x, _y in positions if _x >= self.x]

    def can_attack_pos(self, war_map):
        if self.direction == 0:  # up
            return self.around_pos(war_map) + [(self.x + 2, self.y), (self.x - 2, self.y), (self.x, self.y - 2)]
        if self.direction == 1:  # LEFT
            return self.around_pos(war_map) + [(self.x, self.y + 2), (self.x, self.y - 2), (self.x - 2, self.y)]
        if self.direction == 2:  # DOWN
            return self.around_pos(war_map) + [(self.x + 2, self.y), (self.x - 2, self.y), (self.x, self.y + 2)]
        if self.direction == 3:  # RIGHT
            return self.around_pos(war_map) + [(self.x, self.y + 2), (self.x, self.y - 2), (self.x + 2, self.y)]


class WarMap:
    def __init__(self, blocks: List[Tuple], _my_soldiers: List[Soldier], _op_soldiers: List[Soldier]):
        self.op_soldiers = _op_soldiers
        self.my_soldiers = _my_soldiers
        self.blocks = blocks
        self.pos = [(_x, _y) for owner, _x, _y in blocks]

    def check(self, px, py, _my_soldiers: list):
        soldiers_pos = [(_.x, _.y) for _ in _my_soldiers]
        if ((px, py) in self.pos) and ((px, py) not in soldiers_pos):
            return True
        return False

    def get_owner(self, px, py):
        for owner, _x, _y in self.blocks:
            if px == _x and py == _y:
                return owner

    def set_owner(self, _owner_id):
        pos = list(filter(lambda _: _[1] == self.tx and _[2] == self.ty, self.blocks))[0]
        self.blocks.remove(pos)
        self.blocks.append((_owner_id, self.tx, self.ty))

    def try_move(self, _soldier, soldier_move, _owner_id):
        self.t_soldier = _soldier
        if soldier_move == 'UP':
            self.tx, self.ty = _soldier.x, _soldier.y - 1
        if soldier_move == 'LEFT':
            self.tx, self.ty = _soldier.x - 1, _soldier.y
        if soldier_move == 'DOWN':
            self.tx, self.ty = _soldier.x, _soldier.y + 1
        if soldier_move == 'RIGHT':
            self.tx, self.ty = _soldier.x + 1, _soldier.y
        self.set_owner(_owner_id)
        return self.score()

    def dis_score(self):
        """
        距离分数，距离越近越好
        :return:
        """
        op_pos = filter(lambda _: _[0] == 1 - my_id, self.blocks)
        min_distance = min((abs(self.tx - x) + abs(self.ty - y) for _owner, _x, _y in op_pos))
        return min_distance * (-2)

    def map_score(self):
        """
        盘面分数
        :return:自己的加一分，对方的减一分
        """
        fx = {my_id: 1, -1: 0, 1 - my_id: -1}
        return sum((fx[_[0]] for _ in self.blocks))

    def be_attacked(self):
        """
        被攻击指数
        """
        for _ in self.op_soldiers:
            if (self.tx, self.ty) in _.can_attack_pos(self) and _.level >= self.t_soldier.level:
                return -99999999
        for m in self.my_soldiers:
            for o in self.op_soldiers:
                if (m.x, m.y) in o.can_attack_pos(self) and o.level >= m.level:
                    return -99999999
        return 0

    def score(self):
        return self.map_score() + self.be_attacked() + self.dis_score()


# game loop
while True:
    my_bucks = int(input())  # Your Money
    opp_bucks = int(input())  # Opponent Money
    blocks = []
    for i in range(map_size):
        for j in range(map_size):
            # block_owner: The playerId of this box owned player
            # x: This block's position x
            # y: This block's position y
            block_owner, x, y = [int(k) for k in input().split()]
            blocks.append((block_owner, x, y))

    active_soldier_count = int(input())  # Total no. of active soldier in the game
    my_soldiers = []
    op_soldiers = []
    for i in range(active_soldier_count):
        # owner_id: owner of the soldier
        # x: This soldier's position x
        # y: This soldier's position y
        # soldier_id: The unique identifier of soldier
        # level: Level of the soldier ignore for first league
        # direction: The side where the soldier is facing 0 = UP, 1 = LEFT , 2 = DOWN, 3 = RIGHT
        owner_id, x, y, soldier_id, level, direction = [int(j) for j in input().split()]
        soldier = Soldier(owner_id, x, y, soldier_id, level, direction)
        if soldier.owner_id == my_id:
            my_soldiers.append(soldier)
        else:
            op_soldiers.append(soldier)
    ss = ''
    my_map = WarMap(blocks, my_soldiers, op_soldiers)
    actions = []
    for _ in my_soldiers:
        for move in _.cam_move(my_soldiers + op_soldiers, my_map):
            _map = copy.deepcopy(my_map)
            score = _map.try_move(_, move, my_id)
            actions.append((score, f'MOVE {_.soldier_id} {move} {score}'))

    for _ in my_soldiers:
        for _op in op_soldiers:
            # print(f'{_op.x}{_op.y} att:{_.can_attack()}', file=sys.stderr, flush=True)
            if (_op.x, _op.y) in _.can_attack_pos(my_map) and _.level >= _op.level:
                actions.append((999999999, f'ATTACK {_.soldier_id} {_op.soldier_id}'))

    print(max(actions)[1])
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

# print any of actions - WAIT | MOVE <soldierId> <direction> | ATTACK <soldierID> <soldierId to attack on> | LATER > UPGRADE <id> | DEGRADE <opponent id> | SUICIDE <id>
# print("WAIT")
