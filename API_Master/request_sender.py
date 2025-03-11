import requests
import json

# 通用请求函数，增加 api_name 参数
def send_request(url, headers, api_name, method="POST", params=None, data=None, files=None):
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, data=json.dumps(data) if data else None, files=files)
        response.raise_for_status()
        print(f"{api_name}# Request succeeded")
    except requests.exceptions.HTTPError as errh:
        print(f"{api_name}# Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"{api_name}# Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"{api_name}# Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"{api_name}# Oops: Something Else {err}")