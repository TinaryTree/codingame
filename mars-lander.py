import math
import sys

# Save the Planet.
# Use less Fossil Fuel.

n = int(input())  # the number of points used to draw the surface of Mars.
_y = _x = None
init_inf = []
for i in range(n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    init_inf.append((land_x, land_y))
for land_x, land_y in init_inf:
    if land_y == _y:
        start = _x
        end = land_x
        break
    _x = land_x
    _y = land_y


print(f"{start,end,_y}", file=sys.stderr, flush=True)


class Craft:
    def __init__(self, x, y, hs, vs, f, r, p) -> None:
        self.x = x
        self.y = y
        self.hs = hs
        self.vs = vs
        self.f = f
        self.r = r
        self.p = p

    @property
    def va(self):
        return 3.711/4*p*math.cos(r)

    @property
    def ha(self):
        return 3.711/4*p*math.sin(r)

    @property
    def exp_time(self):
        """
        最短减速时间
        """
        return (40-vs)/self.va
    
    def h_(self):
        if start-x>0:
            


# game loop
while True:

    # hs: the horizontal speed (in m/s), can be negative.
    # vs: the vertical speed (in m/s), can be negative.
    # f: the quantity of remaining fuel in liters.
    # r: the rotation angle in degrees (-90 to 90).
    # p: the thrust power (0 to 4).
    x, y, hs, vs, f, r, p = [int(i) for i in input().split()]
    print(f"{(x, y, hs, vs, f, r, p)}", file=sys.stderr, flush=True)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # R P. R is the desired rotation angle. P is the desired thrust power.
    print(f"{r} 3")
