from get_wrong_way_and_speeding import list_up, list_down

import pandas as pd

df_data = pd.DataFrame()

# 중앙선과 각 차선의 정보
# cctv 별로는 정보는 차후 개발 고려


def get_road_info(tid, cx):

    global list_up, list_down

    if len(list_up) <= 30 or len(list_down) <= 30:
        return None
    df_data["id"] = tid

    min_up_cx, _ = min(list_up)
    max_up_cx, _ = max(list_up)
    min_down_cx, _ = min(list_down)
    max_down_cx, _ = max(list_down)

    # 중앙선 : 양쪽차선의 중앙값
    center_guide_line = (max_down_cx - min_up_cx) / 2
    # 상행선, 하행선 도로 영역 x 좌표 파악 :  오차범위를 고려 +- 20 보정을 하였음
    down_road_range = (min_down_cx - 20, max_down_cx + 20)
    up_road_range = (min_up_cx - 20, max_up_cx + 20)

    # 좌 1차선: max_down_cx + 30
    down_ref_1 = max_down_cx + 30
    down_ref_2 = down_ref_1 - 50
    down_ref_3 = down_ref_2 - 50
    down_ref_4 = down_ref_3 - 50
    down_ref_5 = down_ref_4 - 50
    down_ref_6 = down_ref_5 - 50
    down_ref_7 = down_ref_6 - 50
    down_ref_8 = down_ref_7 - 50

    # 우 1차선 : min_up_cx +30
    up_ref_1 = min_up_cx - 30
    up_ref_2 = up_ref_1 + 50
    up_ref_3 = up_ref_2 + 50
    up_ref_4 = up_ref_3 + 50
    up_ref_5 = up_ref_4 + 50
    up_ref_6 = up_ref_5 + 50
    up_ref_7 = up_ref_6 + 50
    up_ref_8 = up_ref_7 + 50

    # 하행선 차선별 x 축 범위
    in_down_line_1 = down_ref_1 <= cx <= down_ref_2
    in_down_line_2 = down_ref_2 <= cx < down_ref_3
    in_down_line_3 = down_ref_3 <= cx < down_ref_4
    in_down_line_4 = down_ref_4 <= cx < down_ref_5
    in_down_line_5 = down_ref_5 <= cx < down_ref_6
    in_down_line_6 = down_ref_6 <= cx < down_ref_7
    in_down_line_7 = down_ref_7 <= cx < down_ref_8

    # 상행선 차선별 x 축 범위
    in_up_line_1 = up_ref_1 <= cx <= up_ref_2
    in_up_line_2 = up_ref_2 < cx <= up_ref_3
    in_up_line_3 = up_ref_3 < cx <= up_ref_4
    in_up_line_4 = up_ref_4 < cx <= up_ref_5
    in_up_line_5 = up_ref_5 < cx <= up_ref_6
    in_up_line_6 = up_ref_6 < cx <= up_ref_7
    in_up_line_7 = up_ref_7 < cx <= up_ref_8

    # 가상의 차선 파악. 갓길을 고려하여 여분 +-50, 오류 고려하여 +-30
    # 향후 모델학습을 통해 탐지 예정임
    down_line_nums = ((max_down_cx + 30) - (min_down_cx - 50)) // 50
    up_line_nums = (max_up_cx + 50) - (min_up_cx - 30) // 50

    for down_x, _ in list_down:
        if in_down_line_1:
            df_data["line_down_1"].append(down_x)
        elif in_down_line_2:
            df_data["line_down_2"].append(down_x)
        elif in_down_line_3:
            df_data["line_down_3"].append(down_x)
        elif in_down_line_4:
            df_data["line_down_4"].append(down_x)
        elif in_down_line_5:
            df_data["line_down_5"].append(down_x)
        elif in_down_line_6:
            df_data["line_down_6"].append(down_x)
        elif in_down_line_7:
            df_data["line_down_7"].append(down_x)

    for up_x, _ in list_up:
        if in_up_line_1:
            df_data["line_up_1"].append(up_x)
        elif in_up_line_2:
            df_data["line_up_2"].append(up_x)
        elif in_up_line_3:
            df_data["line_up_3"].append(up_x)
        elif in_up_line_4:
            df_data["line_up_4"].append(up_x)
        elif in_up_line_5:
            df_data["line_up_5"].append(up_x)
        elif in_up_line_6:
            df_data["line_up_6"].append(up_x)
        elif in_up_line_7:
            df_data["line_up_7"].append(up_x)
    if center_guide_line:
        print("center guide line")
        return center_guide_line, df_data

    else:
        return None
