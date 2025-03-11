import time
import threading
import queue
import requests
import openai  # 假设这是OpenAI的Python客户端库

openai_api_url = "http://127.0.0.1:8082/v1/chat/completions"
api_key = "sk-xSVYtgauROy87h5u8Fa5SJ0O4Jft58sPZu4yQnsk5c70C0B7B1Fc4969Bd27C9C25308F5Af"


# 请求体结构
class OpenAIRequest:
    def __init__(self, model, prompt, max_tokens, temperature):
        self.model = model
        self.messages = [{"role": "user", "content": prompt}]
        self.max_tokens = max_tokens
        self.temperature = temperature

    def to_dict(self):
        return {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }


def make_request(request_data, response_times_queue):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    start_time = time.time()

    # 注意：这里应该使用openai库的适当方法来发送请求
    # 由于openai库的实际API可能与下面的代码不同，因此这里只是一个示例
    # 你需要根据openai库的文档来构造这个请求
    response = requests.post(openai_api_url, json=request_data.to_dict(), headers=headers)

    if response.status_code != 200:
        print(f"Error response status code: {response.status_code} {response.text}")
    else:
        # 处理响应（如果需要的话）
        pass

    elapsed_time = time.time() - start_time
    response_times_queue.put(elapsed_time)


def run_benchmark(num_requests, concurrent_requests):
    response_times_queue = queue.Queue()
    threads = []

    for i in range(num_requests):
        request_data = OpenAIRequest(model="gpt-4o-mini", prompt="Say hello to OpenAI!", max_tokens=50, temperature=0.7)
        thread = threading.Thread(target=make_request, args=(request_data, response_times_queue))
        threads.append(thread)
        thread.start()

        if i % concurrent_requests == 0:
            # 并没有真正控制请求频率，因为Python的线程在IO密集型任务中表现良好
            # 但如需控制并发数，可以使用线程池或异步IO
            time.sleep(0.1)  # 仅仅为了模拟一点延迟，实际场景中可能不需要

    for thread in threads:
        thread.join()

    total_duration = sum(response_times_queue.get() for _ in range(num_requests))
    average_duration = total_duration / num_requests
    print(f"Average Response Time: {average_duration:.6f} seconds")


if __name__ == "__main__":
    num_requests = 1  # 请求次数（注意：大量请求可能会导致API限制或服务器过载）
    concurrent_requests = 1  # 并发数量（这实际上是线程的数量，但Python的GIL可能会限制真正的并发）

    print(f"Running benchmark with {num_requests} requests and {concurrent_requests} concurrent threads...")
    run_benchmark(num_requests, concurrent_requests)