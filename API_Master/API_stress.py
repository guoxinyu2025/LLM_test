# main.py

import requests
import json
import api_config  # 导入api_requests列表

# 定义一个通用的请求发送函数
def send_request(url, headers, data=None, files=None):
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data) if data else None, files=files)
        response.raise_for_status()
        print("pass")
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else {err}")

# 调用所有接口
if __name__ == "__main__":
    for request in api_config.api_requests:
        send_request(request["url"], request["headers"], data=request.get("data"), files=request.get("files"))