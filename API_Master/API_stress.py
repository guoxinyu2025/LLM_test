# main.py
import api_config  # 导入api_requests列表
import request_sender

# 调用所有接口
if __name__ == "__main__":
    for request in api_config.api_requests:
        method = request.get("method", "POST").upper()  # 默认是POST，可以从配置中获取
        params = request.get("params")  # GET请求的参数
        data = request.get("data")  # POST请求的数据
        files = request.get("files")  # 文件上传
        request_sender.send_request(
            request["url"],
            request["headers"],
            method=method,
            params=params,
            data=data,
            files=files
        )