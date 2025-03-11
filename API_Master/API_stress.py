import api_config
import request_sender

# 调用所有接口
if __name__ == "__main__":
    for request in api_config.api_requests:
        api_name = request.get("name")  # 获取接口名称
        method = request.get("method", "POST").upper()  # 默认是POST，可从配置中获取
        params = request.get("params")
        data = request.get("data")
        files = request.get("files")
        request_sender.send_request(
            request["url"],
            request["headers"],
            api_name,  # 传递接口名称
            method=method,
            params=params,
            data=data,
            files=files
        )