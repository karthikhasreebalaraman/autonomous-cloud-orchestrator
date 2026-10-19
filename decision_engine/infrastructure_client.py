import requests

BASE_URL = "http://localhost:9000"


def get_status():
    response = requests.get(f"{BASE_URL}/status")
    return response.json()


def scale_up():
    response = requests.post(f"{BASE_URL}/scale-up")
    return response.json()


def scale_down():
    response = requests.post(f"{BASE_URL}/scale-down")
    return response.json()


def recover():
    response = requests.post(f"{BASE_URL}/recover")
    return response.json()


def restart():
    response = requests.post(f"{BASE_URL}/restart")
    return response.json()


def replace():
    response = requests.post(f"{BASE_URL}/replace")
    return response.json()


def redistribute():
    response = requests.post(f"{BASE_URL}/redistribute")
    return response.json()