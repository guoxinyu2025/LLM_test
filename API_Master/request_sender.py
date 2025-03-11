# request_sender.py
import requests
import json

# 通用请求函数
def send_request(url, headers, data=None, files=None):
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data) if data else None, files=files)
        response.raise_for_status()
        print("Request succeeded")
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else {err}")