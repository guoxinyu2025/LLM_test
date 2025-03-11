# request_sender.py
import requests
import json

# 通用请求函数
def send_request(url, headers, method="POST", params=None, data=None, files=None):
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:
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
        print(f"Oops: Something Else {err}")