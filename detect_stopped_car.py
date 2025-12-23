import math

vehicle_id = set()
curr_centers = {}
stop_counter = {}


def detect_highway_stopped_vehicle(tid, cx, cy) -> tuple[bool, int] | None:

    if tid not in vehicle_id:
        vehicle_id.add(tid)
        curr_centers[tid] = (cx, cy)
        stop_counter[tid] = 0

        return None

    # 차량 이동 계산
    px, py = curr_centers[tid]
    dx = cx - px
    dy = cy - py
    move_dist = math.hypot(dx, dy)

    curr_centers[tid] = (cx, cy)

    # 차량이동이 없으면 stop_count를 1씩 올린다.
    if move_dist < 0.3:
        stop_counter[tid] += 1

    else:
        pass
    # 10초간 움직임이 없다면 경고하고, 해당 id의 stop_count를 리셋한다.
    if stop_counter[tid] > 300:
        stop_counter[tid] = 0
        return True, tid
    return None


# 라언미;러니ㅏ;란이러재ㅑㄷ라ㅣㅇ라ㅣㅁㄴㅇㄹ재ㅑ랓ㅌ캬ㅐ저ㅏㄹㅇ쟐혀ㅓㅏㅇㄴㄹ거ㅏㅜㅁㅇ냐ㅐ;어ㅜㅏ캬ㅓㅐㄹ4ㄱ3ㄱ래ㅑㅏㅣㄺㄷ쟈ㅏㅣㄺㄷㅈ애ㅑㅏㄷㄱ랴ㅐㅏㅣ
