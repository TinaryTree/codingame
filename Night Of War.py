# Jrke's special
# -Kill your enemy soldiers or Have more bucks than your enemy at end of game
import copy
from typing import List, Tuple

my_id = int(input())  # Your unique player Id
map_size = int(input())  # the size of map MapSize*MapSize

directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


class WarMap:
    def __init__(self, blocks: List[Tuple]):
        self.blocks = blocks
        self.pos = [(_x, _y) for owner, _x, _y in blocks]

    def check(self, px, py, soldiers: list):
        soldiers_pos = [(_.x, _.y) for _ in soldiers]
        if ((px, py) in self.pos) and ((px, py) not in soldiers_pos):
            return True
        return False

    def get_owner(self, px, py):
        for owner, _x, _y in self.blocks:
            if px == _x and py == _y:
                return owner

    def set_owner(self, px, py, owner):
        pos = list(filter(lambda _: _[1] == px and _[2] == py, blocks))[0]
        self.blocks.remove(pos)
        self.blocks.append((owner, px, py))

    def try_move(self, _soldier, soldier_move, owner_id):
        if soldier_move == 'UP':
            self.set_owner(_soldier.x, _soldier.y - 1, owner_id)
        if soldier_move == 'LEFT':
            self.set_owner(_soldier.x - 1, _soldier.y, owner_id)
        if soldier_move == 'DOWN':
            self.set_owner(_soldier.x, _soldier.y + 1, owner_id)
        if soldier_move == 'RIGHT':
            self.set_owner(_soldier.x + 1, _soldier.y, owner_id)


class Soldier:
    def __init__(self, owner_id, x, y, soldier_id, level, direction, war_map: WarMap):
        self.direction = direction
        self.level = level
        self.soldier_id = soldier_id
        self.y = y
        self.x = x
        self.war_map = war_map
        self.owner_id = owner_id

    def cam_move(self, soldiers):
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

    def around_pos(self):
        positions = ((self.x + _x, self.y + _y) for _x, _y in directions)
        positions = ((_x, _y) for _x, _y in positions if self.war_map.check(_x, _y, my_soldiers))
        if self.direction == 0:  # up
            return [(_x, _y) for _x, _y in positions if _y <= self.y]
        if self.direction == 1:  # LEFT
            return [(_x, _y) for _x, _y in positions if _x <= self.x]
        if self.direction == 2:  # DOWN
            return [(_x, _y) for _x, _y in positions if _y >= self.y]
        if self.direction == 3:  # RIGHT
            return [(_x, _y) for _x, _y in positions if _x >= self.x]

    def can_attack(self):
        if self.direction == 0:  # up
            return self.around_pos() + [(self.x + 2, self.y), (self.x - 2, self.y), (self.x, self.y - 2)]
        if self.direction == 1:  # LEFT
            return self.around_pos() + [(self.x, self.y + 2), (self.x, self.y - 2), (self.x - 2, self.y)]
        if self.direction == 2:  # DOWN
            return self.around_pos() + [(self.x + 2, self.y), (self.x - 2, self.y), (self.x, self.y + 2)]
        if self.direction == 3:  # RIGHT
            return self.around_pos() + [(self.x, self.y + 2), (self.x, self.y - 2), (self.x + 2, self.y)]


def evaluate(map: WarMap, soldiers: List[Soldier]):
    fx = {my_id: 1, -1: 0, 1-my_id: -1}
    return sum((fx[_[0]] for _ in map.blocks))


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
    war_map = WarMap(blocks)
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
        soldier = Soldier(owner_id, x, y, soldier_id, level, direction, war_map)
        if soldier.owner_id == my_id:
            my_soldiers.append(soldier)
        else:
            op_soldiers.append(soldier)
    ss = ''
    my_map = WarMap(blocks)
    actions = []
    for _ in my_soldiers:
        for move in _.cam_move(my_soldiers):
            _map = copy.deepcopy(my_map)
            _map.try_move(_, move, my_id)
            score = evaluate(_map, op_soldiers)
            actions.append((score, f'MOVE {_.soldier_id} {move} {score}'))

    for _ in my_soldiers:
        for _op in op_soldiers:
            # print(f'{_op.x}{_op.y} att:{_.can_attack()}', file=sys.stderr, flush=True)
            if (_op.x, _op.y) in _.can_attack():
                actions.append((100, f'ATTACK {_.soldier_id} {_op.soldier_id}'))

    print(max(actions)[1])
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

# print any of actions - WAIT | MOVE <soldierId> <direction> | ATTACK <soldierID> <soldierId to attack on> | LATER > UPGRADE <id> | DEGRADE <opponent id> | SUICIDE <id>
# print("WAIT")
