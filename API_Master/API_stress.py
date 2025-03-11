# main.py

import requests
import json
import api_config  # 导入api_requests列表
import request_sender


# 调用所有接口
if __name__ == "__main__":
    for request in api_config.api_requests:
        request_sender.send_request(request["url"], request["headers"], data=request.get("data"), files=request.get("files"))