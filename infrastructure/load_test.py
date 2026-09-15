import requests
import threading
import time


URL = "http://localhost:5000/cpu"


def send_requests():
    while True:
        try:
            requests.get(URL)
        except:
            pass


for i in range(20):
    thread = threading.Thread(target=send_requests)
    thread.daemon = True
    thread.start()


print("CPU load test started.")
print("Press Ctrl+C to stop.")

while True:
    time.sleep(1)