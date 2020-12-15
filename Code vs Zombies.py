"""Save humans, destroy zombies!"""
# Save humans, destroy zombies!
import math
import sys

shoot = 2000
ash_speed = 1000
zombies_speed = 400


class Zombie:
    """
    Zombie
    """

    def __init__(self, _id, _x, _y, _xnext, _ynext):
        self.id = _id
        self.x = _x
        self.y = _y
        self.xnext = _xnext
        self.ynext = _ynext


class Human:
    """
    Human
    """

    nearest_zombie_id: int

    def __init__(self, _id, _x, _y):
        self.shortest_distance = 0
        self.id = _id
        self.x = _x
        self.y = _y

    def get_nearest_zombies(self, zombies):
        """
        get_nearest_zombies
        :param zombies:
        """
        _ = [calculate_distance(self.x, self.y, zombie.x, zombie.y) for zombie in zombies]
        self.shortest_distance = min(_)
        self.nearest_zombie_id = _.index(self.shortest_distance)

    def can_be_saved(self):
        print("can_be_saved?", file=sys.stderr, flush=True)
        return self.shortest_distance / zombies_speed * ash_speed + shoot >= calculate_distance(x, y, self.x, self.y)


def calculate_distance(x1, y1, x2, y2):
    """
    calculate_distance
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def get_most_dangerous_man(humans):
    shortest_distances = [man.shortest_distance for man in humans]
    shortest_distance = min(shortest_distances)
    most_dangerous_man_id = shortest_distances.index(shortest_distance)
    return humans[most_dangerous_man_id]


# game loop
while True:
    x, y = [int(i) for i in input().split()]
    human_count = int(input())
    humans = []
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        humans.append(Human(human_id, human_x, human_y))
    zombie_count = int(input())
    zombies = []
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombies.append(Zombie(zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext))
    for human in humans:
        human.get_nearest_zombies(zombies)
    humans.sort(key=lambda _human: _human.shortest_distance)
    for human in humans:
        if human.can_be_saved():
            print(human.nearest_zombie_id, file=sys.stderr, flush=True)
            print(f'{zombies[human.nearest_zombie_id].xnext} {zombies[human.nearest_zombie_id].ynext}')
            break
