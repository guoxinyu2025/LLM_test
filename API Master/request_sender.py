import requests
import json

# 通用请求函数，增加 api_name 参数，并返回请求是否成功
def send_request(url, headers, api_name, method="POST", params=None, data=None, files=None):
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, data=json.dumps(data) if data else None, files=files)
        response.raise_for_status()  # 如果状态码不是200，这里会抛出HTTPError
        print(f"{api_name}# Request succeeded")
        return True  # 表示请求成功
    except requests.exceptions.RequestException as err:
        print(f"{api_name}# Error: {err}")
        return False  # 表示请求失败