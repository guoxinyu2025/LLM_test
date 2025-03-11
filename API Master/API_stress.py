import api_config
import request_sender

# 调用所有接口并计算成功率
if __name__ == "__main__":
    total_requests = len(api_config.api_requests)
    successful_requests = 0

    for request in api_config.api_requests:
        api_name = request.get("name")  # 获取接口名称
        method = request.get("method", "POST").upper()  # 默认是POST，可从配置中获取
        params = request.get("params")
        data = request.get("data")
        files = request.get("files")
        headers = request.get("headers")
        url = request["url"]

        # 发送请求并获取是否成功的结果
        is_success = request_sender.send_request(
            url,
            headers,
            api_name,
            method=method,
            params=params,
            data=data,
            files=files
        )

        # 如果请求成功，则增加成功计数
        if is_success:
            successful_requests += 1

    # 计算并打印成功率
    success_rate = (successful_requests / total_requests) * 100
    print(f"Total requests: {total_requests}")
    print(f"Successful requests: {successful_requests}")
    print(f"Success rate: {success_rate:.2f}%")