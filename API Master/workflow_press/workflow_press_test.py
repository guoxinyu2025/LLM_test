import requests
import threading
import time
import json
import random
from datetime import datetime, timedelta
import html
# 注释
# 配置参数
CONCURRENT_THREADS = 1
TEST_DURATION = 10
TARGET_URL = 'https://api.senseflow-test.sensetime.com/v1/workflows/run'
AUTH_TOKEN = 'app-fXWlQDJpS0176MBLv3AOrtnr'

# URL列表
URL_LIST = [
    "https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_828",
    "https://ebui-cdn.cdn.bcebos.com/i18n/zh/layout/yiyan-logo.png",
    "https://gips2.baidu.com/it/u=3128910097,202208282&fm=3030&app=3030&size=re3,2&q=75&n=0&g=4n&f=JPEG&fmt=auto&maxorilen2heic=2000000?s=39843C7AED256A1359D5F4D60000D0B1",
    "https://t9.baidu.com/it/u=583269603,2071876283&fm=217&app=126&size=re3,2&q=75&n=0&g=4n&f=JPEG&fmt=auto&maxorilen2heic=2000000?s=082B5D30151A45CA14D8ECC80100A0B3",
    "https://senseflow-test.sensetime.com/app/create.png",
    "https://senseflow-test.sensetime.com/files/92255965-3e73-483e-8b86-7b893e021c6f/image-compress?timestamp=1749707296&nonce=63ea42b3609e550aecdcd0ec2f1f07a9&sign=MxRu76gsPQNgzYF_eGD3_d_DNUtj4sJocbLfDMz5I_U=",
    "https://senseflow-test.sensetime.com/files/30a7736c-34d0-43d8-be7b-5b1b082391db/image-compress?timestamp=1749707296&nonce=df4623eeb04af1c1cc9343148a56e972&sign=joWHGgfsJt1VRMiMaceO-E5rh61P81vpBm5_tcTrj8s=",
    "https://senseflow-test.sensetime.com/_next/static/media/cover.eacfe46b.png",
    "https://senseflow-test.sensetime.com/files/65a9e41c-2535-4fa3-ac7d-dc3cdde10e64/image-compress?timestamp=1749707388&nonce=f42a2f2b4d859770d2bbc22c441c70e3&sign=HSy2qRHRKKCBwOytsMjx7CRBQ97ZH0CFhmwq1DYg8ks=",
    "https://senseflow-test.sensetime.com/files/51f7482d-9799-44c2-b6a8-7dbf4ce7c738/image-compress?timestamp=1749707388&nonce=e1174bdd5e9ffe21d65048b71c61bd8b&sign=rjMaccxIgJ9LS_wcxIz6FxLRjueZOqQAdD3-sD_Fm8A=",
    "https://senseflow-test.sensetime.com/files/895d2e37-1300-4e7f-a50f-131c0feb2573/image-compress?timestamp=1749707388&nonce=561ec6eaf28026b47c4fe7e4c1f79459&sign=b3ci8FWahEb4snXjXAW9WnZIVyzNKANO4cEWDkZ8V5g=",
    "https://senseflow-test.sensetime.com/files/c3b58b1e-09c9-4899-9432-5a295170bb52/image-compress?timestamp=1749707388&nonce=1d723e6e45dd04a77255ba08c917f380&sign=alWbJuRHOUrtZ1jDs__X_kPtmSS8eYFUtXZd44_2Zdg=",
    "https://himg.bdimg.com/sys/portraitn/item/public.1.608673a6.WTT27DaQtwuPUvUeUHaFKQ?_d=29161787"
]

# 基础请求模板
BASE_REQUEST_BODY = {
    "inputs": {
        "file": None,  # 动态填充
        "a": {
            "dify_model_identity": "__dify__file__",
            "id": None,
            "tenant_id": "fd70f75c-34b8-4bac-9edf-d9b944484068",
            "type": "image",
            "transfer_method": "remote_url",
            "remote_url": None,  # 动态填充
            "related_id": "446c3728-30ca-4f23-8719-2b7f86ec0db6",
            "filename": "logo.png",
            "extension": ".png",
            "mime_type": "image/png",
            "size": 8669,
            "url": None  # 动态填充
        }
    },
    "user": "abc-123",
    "response_mode": "streaming"
}

# 扩展统计信息结构
stats = {
    'success': 0,
    'error': 0,
    'requests': [],
    'response_times': [],
    'lock': threading.Lock(),
    'min_response_time': float('inf'),  # 初始化最小响应时间为无穷大
    'max_response_time': 0,  # 初始化最大响应时间为0
    'total_response_time': 0  # 初始化总响应时间
}

start_time = datetime.now()
end_time = start_time + timedelta(seconds=TEST_DURATION)


def save_to_log_file(filename):
    """将请求记录保存到日志文件"""
    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write("时间戳,URL,状态码,响应时间(ms),响应内容\n")
        for req in stats['requests']:
            timestamp = req['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            url = req['url']
            status_code = req['status_code']
            response_time = f"{req['response_time']:.2f}"
            # 直接写入原始响应内容，不进行HTML转义
            response_content = str(req['response_content']).replace('\n', '\\n').replace('\r', '\\r')
            f.write(f"{timestamp},{url},{status_code},{response_time},{response_content}\n")


def create_html_report(filename):
    """生成包含详细请求记录的HTML测试报告"""
    # 计算统计指标
    total = len(stats['requests'])
    success = sum(1 for r in stats['requests'] if r['status_code'] == 200)
    error = total - success
    qps = success / TEST_DURATION if TEST_DURATION > 0 else 0

    # 计算响应时间统计
    min_time = min(stats['response_times']) if stats['response_times'] else 0
    max_time = max(stats['response_times']) if stats['response_times'] else 0
    avg_time = sum(stats['response_times']) / len(stats['response_times']) if stats['response_times'] else 0

    # 准备请求数据
    requests_data = []
    for req in stats['requests']:
        # 保留完整响应内容（不再截断）
        response_content = str(req['response_content'])
        requests_data.append({
            'timestamp': req['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'url': req['url'],
            'status_code': req['status_code'],
            'response_time': f"{req['response_time']:.2f}ms",
            'status': 'SUCCESS' if req['status_code'] == 200 else 'FAIL',
            'response_content': response_content  # 完整内容
        })

    # 生成HTML内容（使用UTF-8编码）
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>API压力测试报告 - {datetime.now().strftime('%Y%m%d%H%M%S')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .summary {{ border: 1px solid #ddd; padding: 20px; margin-bottom: 30px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f5f5f5; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .status-success {{ color: green; }}
            .status-error {{ color: red; }}
            .timestamp {{ font-size: 0.9em; color: #666; }}
            .response-content {{
                max-height: 300px;
                overflow: auto;
                white-space: pre-wrap;
                word-break: break-all;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <h1>API压力测试报告</h1>
        <div class="summary">
            <h2>测试摘要</h2>
            <p>测试开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>总请求数: {total}</p>
            <p>成功请求: {success}</p>
            <p>失败请求: {error}</p>
            <p>QPS: {qps:.2f} req/sec</p>
            <p>平均响应时间: {avg_time:.2f} 毫秒</p>
            <p>最快响应: {min_time:.2f} 毫秒</p>
            <p>最慢响应: {max_time:.2f} 毫秒</p>
        </div>

        <h2>请求明细（显示前500条）</h2>
        <table>
            <tr>
                <th>时间戳</th>
                <th>URL</th>
                <th>状态码</th>
                <th>响应时间</th>
                <th>状态</th>
                <th>响应内容</th>
            </tr>
            {''.join([f'''
            <tr>
                <td class="timestamp">{row["timestamp"]}</td>
                <td>{row["url"]}</td>
                <td>{row["status_code"]}</td>
                <td>{row["response_time"]}</td>
                <td class="status-{row["status"].lower()}">{row["status"]}</td>
                <td class="response-content">{html.escape(row["response_content"])}</td>
            </tr>
            ''' for row in requests_data[:500]])}
        </table>
    </body>
    </html>
    """

    # 写入报告文件（使用UTF-8编码）
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)


def create_request_body():
    """创建动态请求体"""
    url = random.choice(URL_LIST)
    body = BASE_REQUEST_BODY.copy()
    body["inputs"]["a"]["remote_url"] = url
    body["inputs"]["a"]["url"] = url
    return body


def pressure_test(session):
    global stats
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json'
    }

    while datetime.now() < end_time:
        try:
            start_time = time.time()
            request_body = create_request_body()
            url = random.choice(URL_LIST)

            response = session.post(
                TARGET_URL,
                headers=headers,
                json=request_body,
                timeout=30
            )

            response_time = (time.time() - start_time) * 1000

            # 记录完整响应内容
            full_response_content = response.text

            # 强制UTF-8解码
            try:
                full_response_content = response.content.decode('utf-8')
            except:
                full_response_content = response.text

            with stats['lock']:
                # 更新响应时间统计
                if response_time < stats['min_response_time']:
                    stats['min_response_time'] = response_time
                if response_time > stats['max_response_time']:
                    stats['max_response_time'] = response_time
                stats['total_response_time'] += response_time

                stats['requests'].append({
                    'timestamp': datetime.now(),
                    'url': url,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'response_content': full_response_content
                })
                stats['response_times'].append(response_time)

                # 更新统计计数
                if response.status_code == 200:
                    stats['success'] += 1
                else:
                    stats['error'] += 1

        except Exception as e:
            with stats['lock']:
                stats['error'] += 1
                stats['requests'].append({
                    'timestamp': datetime.now(),
                    'url': '',
                    'status_code': 500,
                    'response_time': -1,
                    'response_content': f'请求失败: {str(e)}'
                })


def main():
    global end_time
    with requests.Session() as session:
        threads = []
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=TEST_DURATION)

        # 启动工作线程
        for _ in range(CONCURRENT_THREADS):
            thread = threading.Thread(target=pressure_test, args=(session,))
            threads.append(thread)
            thread.start()

        # 等待测试结束
        while datetime.now() < end_time:
            time.sleep(1)
            elapsed = (datetime.now() - start_time).total_seconds()
            remaining = max(0, (end_time - datetime.now()).total_seconds())
            print(f"\r进度: {elapsed:.0f}/{TEST_DURATION}s | 剩余: {remaining:.0f}s", end="")

        # 停止所有线程
        for thread in threads:
            thread.join()

    # 生成报告和日志文件
    report_filename = f"pressure_test_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    log_filename = f"pressure_test_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    create_html_report(report_filename)
    save_to_log_file(log_filename)

    print(f"\n\n测试报告已生成: {report_filename}")
    print(f"详细日志已生成: {log_filename}")

    # 计算平均响应时间
    avg_response_time = stats['total_response_time'] / (stats['success'] + stats['error']) if (stats['success'] + stats[
        'error']) > 0 else 0

    # 输出统计结果（添加响应时间统计）
    print("\n\n=== 压力测试结果 ===")
    print(f"总请求数: {stats['success'] + stats['error']}")
    print(f"成功请求: {stats['success']}")
    print(f"失败请求: {stats['error']}")
    print(f"持续时间: {TEST_DURATION} 秒")
    print(f"并发数: {CONCURRENT_THREADS} 线程")
    print(f"QPS: {stats['success'] / TEST_DURATION:.2f} req/sec")

    # 新增：打印响应时间统计
    print("\n=== 响应时间统计 ===")
    print(f"最小响应速度: {stats['min_response_time']:.2f} 毫秒")
    print(f"最大响应速度: {stats['max_response_time']:.2f} 毫秒")
    print(f"平均响应时间: {avg_response_time:.2f} 毫秒")


if __name__ == "__main__":
    main()