# request_sender
import requests
import json

# # 通用请求函数，增加 api_name 参数，并返回请求是否成功
# def send_request(url, headers, api_name, method="POST", params=None, data=None, files=None):
#     try:
#         if method.upper() == "GET":
#             response = requests.get(url, headers=headers, params=params)
#         else:
#             response = requests.post(url, headers=headers, data=json.dumps(data) if data else None, files=files)
#         response.raise_for_status()  # 如果状态码不是200，这里会抛出HTTPError
#         print(f"{api_name}# Request succeeded")
#         return True  # 表示请求成功
#     except requests.exceptions.RequestException as err:
#         print(f"{api_name}# Error: {err}")
#         return False  # 表示请求失败

import requests
import json
import time


def send_request(url, headers, api_name, method="POST", params=None, data=None, files=None):
    start_time = time.time()
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, data=json.dumps(data) if data else None, files=files)
        response.raise_for_status()
        end_time = time.time()
        response_time = end_time - start_time
        response_content = response.text[:500]  # 限制内容长度以避免HTML文件过大
        print(f"{api_name}# Request succeeded in {response_time:.4f}s")
        return True, response_time, response_content
    except requests.exceptions.RequestException as err:
        end_time = time.time()
        response_time = end_time - start_time  # Still record time taken even if failed
        print(f"{api_name}# Error: {err}")
        return False, response_time, None

