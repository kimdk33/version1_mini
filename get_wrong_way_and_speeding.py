import numpy as np
import pandas as pd
from collections import deque
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression


# model = LinearRegression()


dq_up = deque(maxlen=200)
dq_down = deque(maxlen=200)

df_px_speed = pd.DataFrame(columns=["up", "up_target", "down", "down_target"])


def wrong_way_drive(tid, cls, cx, cy, car_direction, speed_px1):
    global dq_up, dq_down, df_px_speed
    speed_constant = 110 / speed_px1

    if car_direction == "up":
        if cls == 2:
            df_px_speed[tid, ["up", "up_target"]] = [cx, speed_constant]
        dq_up.append([cx, cy])
        direction = 1

    elif car_direction == "down":
        if cls == 2:
            df_px_speed[tid, ["down", "down_target"]] = [cx, speed_constant]
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


def get_real_speed(cx):
    global df_px_speed
    up_num: int = df_px_speed["up"].count()
    down_num: int = df_px_speed["down"].count()

    if up_num < 30 or down_num < 30:
        return None

    else:

        col1 = "up"

        q_up = df_px_speed[col1].quantile(0.25)
        q3_up = df_px_speed[col1].quantile(0.75)
        iqr_up = q3_up - q_up

        df_up = df_px_speed[
            (df_px_speed[col1] >= q_up - 1.5 * iqr_up)
            & (df_px_speed[col1] <= q3_up + 1.5 * iqr_up)
        ]

        ave1 = df_up.mean()
        target_ave_1 = df_up["up_target"].mean()

        col2 = "down"

        q_down = df_px_speed[col2].quantile(0.25)
        q3_down = df_px_speed[col2].quantile(0.75)
        iqr_down = q3_down - q_down

        df_down = df_px_speed[
            (df_px_speed[col2] >= q_down - 1.5 * iqr_down)
            & (df_px_speed[col2] <= q3_down + 1.5 * iqr_down)
        ]

        ave2 = df_down.mean()
        target_ave_2 = df_down["down_target"].mean()

        data = [
            [ave1],
            [ave2],
        ]

        data_target = [target_ave_1, target_ave_2]
        model = LinearRegression()
        model.fit(data, data_target)
        real_speed = model.predict([[cx]])
        # print('기울기', model.coef_)  # [w1, w2]
        # print('y절편', model.intercept_)
        # print('원하는 값', real_speed)

        return real_speed
