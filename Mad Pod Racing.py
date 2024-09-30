import sys
import math

# 解析输入
checkpoints = {}
laps = int(input())  # 圈数
checkpoint_count = int(input())  # 检查点数
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoints[i] = (checkpoint_x, checkpoint_y)

def dist(x1, y1, x2, y2):
    """ 计算两点间距离 """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def aim_angle(x1, y1, x2, y2):
    """ 计算夹角 """
    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg if angle_deg >= 0 else angle_deg + 360

class Pod:
    def __init__(self):
        self.x = None
        self.y = None
        self.vx = None
        self.vy = None
        self.angle = None
        self.next_check_point_id = None

    def update_status(self, x, y, vx, vy, angle, next_check_point_id):
        """ 更新最新状态 """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = angle
        self.next_check_point_id = next_check_point_id

    def speed(self):
        """ 计算速度大小 """
        return math.sqrt(self.vx ** 2 + self.vy ** 2)

    def aim_angle(self, target_checkpoint_id):
        """ 计算朝向目标检查点的角度 """
        checkpoint = checkpoints[target_checkpoint_id]
        return aim_angle(self.x, self.y, checkpoint[0], checkpoint[1])

    def should_turn_to_next(self):
        """ 判断是否应该提前转向下一个检查点 """
        next_checkpoint = checkpoints[self.next_check_point_id]
        distance_to_next = dist(self.x, self.y, *next_checkpoint)

        # 检查是否需要提前转向（根据距离和速度动态调整）
        if distance_to_next < 2000 and self.speed() > 300:
            return True
        return False

    def adjust_thrust_based_on_angle(self, angle_diff):
        """ 根据角度差调整推力 """
        # 根据角度差调整推力
        if angle_diff >= 90:
            return 0  # 如果与目标角度差距大于等于90度，推力为0
        elif angle_diff == 0:
            return 100  # 如果与目标角度完全一致，推力为100
        else:
            # 在0到90度之间，推力与角度差成反比关系
            return int(100 * (1 - (angle_diff / 90)))  # 反比关系

    def analyze_trajectory(self):
        """ 通过速度向量和距离分析轨迹，确保能够通过检查点 """
        next_checkpoint = checkpoints[self.next_check_point_id]
        distance_to_checkpoint = dist(self.x, self.y, *next_checkpoint)

        # 分析当前位置与速度向量是否可能错过检查点
        if distance_to_checkpoint < 1000 and self.speed() > 400:
            return 30  # 靠近检查点时强制减速
        return self.thrust()

    def thrust(self):
        """ 根据与目标夹角大小，计算推力 """
        target_angle = self.aim_angle(self.next_check_point_id)
        angle_diff = abs(self.angle - target_angle)

        # 动态调整推力
        return self.adjust_thrust_based_on_angle(angle_diff)

    def aim(self):
        """ 计算目标点坐标 """
        if self.should_turn_to_next():
            # 提前朝向下一个检查点
            next_id = (self.next_check_point_id + 1) % checkpoint_count
            return checkpoints[next_id]
        else:
            # 朝向当前的检查点
            return checkpoints[self.next_check_point_id]

    def check_collision(self, opponent_pods):
        """ 检查是否有可能与对手的 Pod 碰撞 """
        for opponent_pod in opponent_pods:
            distance_to_opponent = dist(self.x, self.y, opponent_pod.x, opponent_pod.y)

            # 如果两 Pod 距离小于 800，则可能碰撞
            if distance_to_opponent < 850:
                return True  # 速度较高且距离较近，启用盾牌
        return False


# 初始化 pod
pods = [Pod() for _ in range(2)]
op_pods = [Pod() for _ in range(2)]

# 主循环
while True:
    for i in range(2):
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]
        pods[i].update_status(x, y, vx, vy, angle, next_check_point_id)

    for i in range(2):
        x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2 = [int(j) for j in input().split()]
        op_pods[i].update_status(x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2)

    for i in range(2):
        target_x, target_y = pods[i].aim()

        # 检查是否即将与对手碰撞
        if pods[i].check_collision(op_pods):
            # 如果即将发生碰撞，则启用盾牌
            print(f"{int(target_x)} {int(target_y)} SHIELD")
        else:
            # 正常计算推力并输出坐标和推力
            thrust_value = pods[i].analyze_trajectory()
            print(f"{int(target_x)} {int(target_y)} {thrust_value}")
