"""
Traffic Anomalies API 요청 테스트 예시
"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000/api"


def test_post_anomaly_with_file():
    """파일과 함께 anomaly POST 요청"""
    url = f"{BASE_URL}/traffic_anomalies"

    # form 데이터
    data = {
        "type": "불법주차",
        "cctv_id": "1",
        "detected_at": datetime.now().isoformat(),
    }

    # 파일 첨부 (영상 또는 이미지)
    files = {
        "file": ("./manimani.mp4", open("./manimani.mp4", "rb"), "video/mp4")
    }

    response = requests.post(url, data=data, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def test_post_anomaly_without_file():
    """파일 없이 anomaly POST 요청"""
    url = f"{BASE_URL}/traffic_anomalies"

    data = {
        "type": "사고",
        "cctv_id": "1",
        "detected_at": datetime.now().isoformat(),
    }

    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def test_get_anomalies():
    """모든 anomaly 조회"""
    url = f"{BASE_URL}/traffic_anomalies"

    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


if __name__ == "__main__":
    print("=== GET all anomalies ===")
    test_get_anomalies()

    # print("\n=== POST anomaly without file ===")
    # test_post_anomaly_without_file()

    # 파일이 있을 경우에만 실행
    print("\n=== POST anomaly with file ===")
    test_post_anomaly_with_file()