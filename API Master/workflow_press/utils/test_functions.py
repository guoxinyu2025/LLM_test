import threading
import time
import requests
import random
from datetime import datetime
from url_config import URL_LIST

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

def display_progress(stats, test_start_time, test_duration_seconds):
    """显示实时进度"""
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

def make_request(template, stats, test_start_time, test_duration_seconds, target_url, auth_token):
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
                target_url,
                headers={
                    'Authorization': f'Bearer {auth_token}',
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