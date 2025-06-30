import requests
import threading
import time
import json
import random
from datetime import datetime, timedelta
import html
from html_report_generator import create_html_report
from url_config import URL_LIST
from request_templates import get_template, print_available_templates, list_available_templates

# 注释
# 配置参数
CONCURRENT_THREADS = 1
TEST_DURATION = 10
TARGET_URL = 'https://api.senseflow-test.sensetime.com/v1/workflows/run'
AUTH_TOKEN = 'app-IrCFq1GXD9ZbG6xSK9shqTiZ'

# 移除原有的BASE_REQUEST_BODY，改为动态获取

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

# 全局变量用于进度显示
test_start_time = None
test_duration_seconds = TEST_DURATION
selected_template = None  # 存储选择的模板

def select_request_template():
    """让用户选择请求体模板"""
    print_available_templates()
    
    while True:
        try:
            choice = input("请选择请求体模板 (输入模板名称或编号): ").strip()
            
            # 如果输入的是数字，转换为模板名称
            if choice.isdigit():
                template_list = list_available_templates()
                index = int(choice) - 1
                if 0 <= index < len(template_list):
                    choice = template_list[index]
                else:
                    print(f"无效的编号，请输入1-{len(template_list)}之间的数字")
                    continue
            
            # 获取模板
            template = get_template(choice)
            print(f"已选择模板: {choice}")
            return template, choice
            
        except ValueError as e:
            print(f"错误: {e}")
            print("请重新选择")
        except KeyboardInterrupt:
            print("\n用户取消选择")
            exit(0)

def format_time(seconds):
    """格式化时间显示"""
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}分{remaining_seconds:.1f}秒"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        return f"{hours}小时{minutes}分{remaining_seconds:.1f}秒"

def display_progress():
    """显示实时进度"""
    global test_start_time, test_duration_seconds
    
    while True:
        if test_start_time is None:
            time.sleep(0.1)
            continue
            
        elapsed = (datetime.now() - test_start_time).total_seconds()
        remaining = max(0, test_duration_seconds - elapsed)
        progress_percent = min(100, (elapsed / test_duration_seconds) * 100)
        
        # 获取当前统计信息
        with stats['lock']:
            total_requests = len(stats['requests'])
            success_count = stats['success']
            error_count = stats['error']
            current_qps = success_count / elapsed if elapsed > 0 else 0
        
        # 清除当前行并显示进度
        print(f"\r[进度: {progress_percent:.1f}%] 已运行: {format_time(elapsed)} | 剩余: {format_time(remaining)} | 总请求: {total_requests} | 成功: {success_count} | 失败: {error_count} | 当前QPS: {current_qps:.2f}", end='', flush=True)
        
        # 如果测试结束，退出循环
        if elapsed >= test_duration_seconds:
            print()  # 换行
            break
            
        time.sleep(1)  # 每秒更新一次

def make_request(template):
    """发送单个请求的函数"""
    while True:
        # 检查是否测试时间已到
        if test_start_time and (datetime.now() - test_start_time).total_seconds() >= test_duration_seconds:
            break
            
        # 随机选择一个URL
        url = random.choice(URL_LIST)
        
        # 构建请求体
        request_body = template.copy()
        
        # 根据模板类型填充不同的字段
        if 'file' in request_body.get('inputs', {}):
            request_body['inputs']['file'] = url
        if 'a' in request_body.get('inputs', {}):
            if 'remote_url' in request_body['inputs']['a']:
                request_body['inputs']['a']['remote_url'] = url
            if 'url' in request_body['inputs']['a']:
                request_body['inputs']['a']['url'] = url
        if 'image' in request_body.get('inputs', {}):
            request_body['inputs']['image'] = url
        if 'text' in request_body.get('inputs', {}):
            request_body['inputs']['text'] = f"测试文本内容 - {url[:20]}"
        if 'document' in request_body.get('inputs', {}):
            request_body['inputs']['document'] = url
        
        # 记录请求开始时间
        start_time = datetime.now()
        
        try:
            # 发送请求
            response = requests.post(
                TARGET_URL,
                headers={
                    'Authorization': f'Bearer {AUTH_TOKEN}',
                    'Content-Type': 'application/json'
                },
                json=request_body,
                timeout=30
            )
            
            # 计算响应时间
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000  # 转换为毫秒
            
            # 获取响应内容
            response_content = response.text
            
            # 线程安全地更新统计信息
            with stats['lock']:
                if response.status_code == 200:
                    stats['success'] += 1
                else:
                    stats['error'] += 1
                
                # 记录请求详情
                stats['requests'].append({
                    'timestamp': start_time,
                    'url': url,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'response_content': response_content
                })
                
                # 更新响应时间统计
                stats['response_times'].append(response_time)
                stats['min_response_time'] = min(stats['min_response_time'], response_time)
                stats['max_response_time'] = max(stats['max_response_time'], response_time)
                stats['total_response_time'] += response_time
                
                # 打印实时状态（只在详细模式下显示）
                # total_requests = len(stats['requests'])
                # print(f"请求 {total_requests}: URL={url[:50]}..., 状态码={response.status_code}, 响应时间={response_time:.2f}ms")
                
        except Exception as e:
            # 记录错误
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            with stats['lock']:
                stats['error'] += 1
                stats['requests'].append({
                    'timestamp': start_time,
                    'url': url,
                    'status_code': 0,  # 0表示网络错误
                    'response_time': response_time,
                    'response_content': f"Error: {str(e)}"
                })
                stats['response_times'].append(response_time)
                stats['min_response_time'] = min(stats['min_response_time'], response_time)
                stats['max_response_time'] = max(stats['max_response_time'], response_time)
                stats['total_response_time'] += response_time
                
                # 打印错误信息（只在详细模式下显示）
                # total_requests = len(stats['requests'])
                # print(f"请求 {total_requests}: URL={url[:50]}..., 错误: {str(e)}")

def main():
    """主函数"""
    global test_start_time, test_duration_seconds
    
    print(f"开始API压力测试...")
    print(f"目标URL: {TARGET_URL}")
    print(f"并发线程数: {CONCURRENT_THREADS}")
    print(f"测试持续时间: {TEST_DURATION}秒")
    print(f"URL池大小: {len(URL_LIST)}")
    print("-" * 50)
    
    # 选择请求体模板
    selected_template, template_name = select_request_template()
    
    # 记录测试开始时间
    test_start_time = datetime.now()
    
    # 创建并启动进度显示线程
    progress_thread = threading.Thread(target=display_progress)
    progress_thread.daemon = True
    progress_thread.start()
    
    # 创建并启动请求线程
    threads = []
    for i in range(CONCURRENT_THREADS):
        thread = threading.Thread(target=make_request, args=(selected_template,))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 等待进度显示线程完成
    progress_thread.join()
    
    # 记录测试结束时间
    end_time = datetime.now()
    
    # 计算测试持续时间
    test_duration = (end_time - test_start_time).total_seconds()
    
    # 生成统计报告
    total_requests = len(stats['requests'])
    success_count = stats['success']
    error_count = stats['error']
    
    if stats['response_times']:
        avg_response_time = sum(stats['response_times']) / len(stats['response_times'])
        min_response_time = min(stats['response_times'])
        max_response_time = max(stats['response_times'])
    else:
        avg_response_time = min_response_time = max_response_time = 0
    
    qps = success_count / test_duration if test_duration > 0 else 0
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)
    print(f"使用的模板: {template_name}")
    print(f"总请求数: {total_requests}")
    print(f"成功请求: {success_count}")
    print(f"失败请求: {error_count}")
    print(f"成功率: {(success_count/total_requests*100):.2f}%" if total_requests > 0 else "成功率: 0%")
    print(f"QPS: {qps:.2f} req/sec")
    print(f"平均响应时间: {avg_response_time:.2f}ms")
    print(f"最快响应时间: {min_response_time:.2f}ms")
    print(f"最慢响应时间: {max_response_time:.2f}ms")
    print(f"测试持续时间: {test_duration:.2f}秒")
    
    # 生成HTML报告
    report_filename = f"api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    create_html_report(report_filename, stats, test_duration, CONCURRENT_THREADS, test_start_time, end_time)
    print(f"\nHTML报告已生成: {report_filename}")

if __name__ == "__main__":
    main()