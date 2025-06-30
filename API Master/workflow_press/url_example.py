#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL配置使用示例
展示如何使用url_config模块中的功能
"""

from url_config import URL_LIST, get_url_list, add_url, remove_url, get_url_count
import random

def main():
    """主函数 - 展示URL配置的使用方法"""
    
    print("=== URL配置使用示例 ===\n")
    
    # 1. 获取URL列表
    print("1. 获取所有URL:")
    urls = get_url_list()
    for i, url in enumerate(urls, 1):
        print(f"   {i:2d}. {url[:60]}...")
    print()
    
    # 2. 获取URL数量
    count = get_url_count()
    print(f"2. URL总数: {count}")
    print()
    
    # 3. 随机选择一个URL
    random_url = random.choice(URL_LIST)
    print(f"3. 随机选择的URL: {random_url[:80]}...")
    print()
    
    # 4. 添加新URL
    new_url = "https://example.com/test-image.jpg"
    print(f"4. 尝试添加新URL: {new_url}")
    if add_url(new_url):
        print("   ✓ 添加成功")
    else:
        print("   ✗ URL已存在")
    print()
    
    # 5. 再次获取URL数量
    new_count = get_url_count()
    print(f"5. 添加后的URL总数: {new_count}")
    print()
    
    # 6. 移除URL
    print(f"6. 尝试移除URL: {new_url}")
    if remove_url(new_url):
        print("   ✓ 移除成功")
    else:
        print("   ✗ URL不存在")
    print()
    
    # 7. 最终URL数量
    final_count = get_url_count()
    print(f"7. 移除后的URL总数: {final_count}")
    print()
    
    print("=== 示例完成 ===")

if __name__ == "__main__":
    main() 