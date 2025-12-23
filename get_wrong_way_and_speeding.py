import numpy as np
import pandas as pd
from collections import deque
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression


# model = LinearRegression()


dq_up = deque(maxlen=200)
dq_down = deque(maxlen=200)

df_px_speed = pd.DataFrame(
    columns=["up_x", "up_y", "up_target", "down_x", "down_y", "down_target"]
)


def wrong_way_drive(tid, cls, cx, cy, car_direction, speed_px1):
    global dq_up, dq_down, df_px_speed
    speed_constant = 110 / speed_px1

    if car_direction == "up":
        if (cls == 2) and (len(df_px_speed) < 1000):
            df_px_speed.loc[tid, "up_x"] = cx
            df_px_speed.loc[tid, "up_y"] = cy
            df_px_speed.loc[tid, "up_target"] = speed_constant
        dq_up.append([cx, cy])
        print("방향 개수", len(dq_up))
        direction = 1

    elif car_direction == "down":
        if (cls == 2) and (len(df_px_speed) < 1000):
            df_px_speed.loc[tid, "down_x"] = cx
            df_px_speed.loc[tid, "down_y"] = cy
            df_px_speed.loc[tid, "down_target"] = speed_constant

        dq_down.append([cx, cy])
        print("방향 개수", len(dq_down))
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


# model_up = None
# model_down = None

num = 0


def get_real_speed(cx, cy, direction):
    global df_px_speed, num
    print(" 데이터 프페임의 개수는", len(df_px_speed))
    up_num: int = df_px_speed["up_target"].count()
    down_num: int = df_px_speed["down_target"].count()

    # df_px_speed[tid, ["up_x","up_y" , "up_target"]]

    if up_num < 30 or down_num < 30:
        num += 1
        print(f"속도보정 학습중 {num}")
        return None

    else:
        if direction == "up":
            if len(df_px_speed) <= 998:
                col1 = "up_target"

                q_up = df_px_speed[col1].quantile(0.25)
                q3_up = df_px_speed[col1].quantile(0.75)
                iqr_up = q3_up - q_up

                df_up = df_px_speed[
                    (df_px_speed[col1] >= q_up - 1.5 * iqr_up)
                    & (df_px_speed[col1] <= q3_up + 1.5 * iqr_up)
                ]

                data = [[x, y] for x, y in zip(df_up["up_x"], df_up["up_y"])]

                # print(data)

                data_target = [x for x in df_up["up_target"]]

                model_up = LinearRegression()
                model_up.fit(data, data_target)

                real_speed_constant = model_up.predict([[cx, cy]])
                # print('기울기', model.coef_)  # [w1, w2]
                # print('y절편', model.intercept_)
                # print('원하는 값', real_speed)

                return real_speed_constant

        else:

            if len(df_px_speed) <= 998:
                col2 = "down_target"

                q_down = df_px_speed[col2].quantile(0.25)
                q3_down = df_px_speed[col2].quantile(0.75)
                iqr_down = q3_down - q_down

                df_down = df_px_speed[
                    (df_px_speed[col2] >= q_down - 1.5 * iqr_down)
                    & (df_px_speed[col2] <= q3_down + 1.5 * iqr_down)
                ]

                data = [[x, y] for x, y in zip(df_down["down_x"], df_down["down_y"])]

                data_target = [x for x in df_down["down_target"]]

                model_down = LinearRegression()
                model_down.fit(data, data_target)
                real_speed_constant = model_down.predict([[cx, cy]])
                # print('기울기', model.coef_)  # [w1, w2]
                # print('y절편', model.intercept_)
                # print('원하는 값', real_speed)

                return real_speed_constant
