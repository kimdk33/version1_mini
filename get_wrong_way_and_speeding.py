
import numpy as np
from collections import deque
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression


# model = LinearRegression()


dq_up = deque(maxlen=100)
dq_down = deque(maxlen=100)


list_up = []
list_up_target = []
list_down = []
list_down_target = []


def wrong_way_drive(cls, cx, cy, car_direction, speed_px1):
    global dq_up, dq_down, list_up, list_up_target, list_down, list_down_target
    speed_constant = 110/speed_px1

    if car_direction == "up":
        if cls == 2:
            list_up.append(cx)
            list_up_target.append(speed_constant)
        dq_up.append([cx, cy])
        direction = 1

    elif car_direction == "down":
        if cls == 2:
            list_down.append(cx)
            list_down_target.append(speed_constant)
        dq_down.append([cx, cy])
        direction = 0
    else:
        return None

    if len(dq_up) <= 30 or len(dq_down) <= 30:
        return None

    qp_all = np.concatenate((dq_up, dq_down))
    target = [1] * len(dq_up) + [0] * len(dq_down)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(qp_all, target)

    result = knn.predict([[cx, cy]])
    # 탐지 방향과 근접분류 방향이 같지 않으면 역주행으로 간주
    if result[0] != direction:
        detect_wrong_way = True
        return detect_wrong_way
    else:
        return None

def get_real_speed(cls, cx):
    global list_up, list_up_target, list_down, list_down_target

    if len(list_up) < 30 or len(list_down) < 30 :
        return None

    else:
        length1 = len(list_up)
        data_ave_1 = sum(list_up) / (length1*20)
        target_ave_1 = sum(list_up_target) / length1
        length2 = len(list_down)
        data_ave_2 = sum(list_down) / (length2*20)
        target_ave_2 = sum(list_down_target) / length2

        data = [
            [data_ave_1],
            [data_ave_2],
        ]

        data_target = [target_ave_1, target_ave_2]
        model = LinearRegression()
        model.fit(data, data_target)
        real_speed = model.predict([[cx/20]])
        # print('기울기', model.coef_)  # [w1, w2]
        # print('y절편', model.intercept_)
        # print('원하는 값', real_speed)

        return real_speed


