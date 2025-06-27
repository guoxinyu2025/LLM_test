import html
from datetime import datetime


def create_html_report(filename, stats, test_duration, concurrent_threads, start_time, end_time):
    """生成包含详细请求记录的HTML测试报告"""
    # 计算统计指标
    total = len(stats['requests'])
    success = sum(1 for r in stats['requests'] if r['status_code'] == 200)
    error = total - success
    qps = success / test_duration if test_duration > 0 else 0

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
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                line-height: 1.6;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
                animation: fadeInDown 1s ease-out;
            }}
            
            .header h1 {{
                color: white;
                font-size: 2.5rem;
                font-weight: 300;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            
            .header p {{
                color: rgba(255,255,255,0.9);
                font-size: 1.1rem;
            }}
            
            .summary {{
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                animation: fadeInUp 1s ease-out 0.3s both;
            }}
            
            .summary h2 {{
                color: #2c3e50;
                margin-bottom: 25px;
                font-size: 1.8rem;
                font-weight: 500;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                animation: fadeInUp 1s ease-out 0.5s both;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 30px rgba(0,0,0,0.2);
            }}
            
            .stat-card h3 {{
                font-size: 2rem;
                font-weight: 300;
                margin-bottom: 5px;
            }}
            
            .stat-card p {{
                font-size: 0.9rem;
                opacity: 0.9;
            }}
            
            .success {{
                background: linear-gradient(135deg, #56ab2f, #a8e6cf);
            }}
            
            .error {{
                background: linear-gradient(135deg, #ff416c, #ff4b2b);
            }}
            
            .info {{
                background: linear-gradient(135deg, #4facfe, #00f2fe);
            }}
            
            .performance {{
                background: linear-gradient(135deg, #fa709a, #fee140);
            }}
            
            .table-section {{
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                animation: fadeInUp 1s ease-out 0.7s both;
            }}
            
            .table-section h2 {{
                color: #2c3e50;
                margin-bottom: 25px;
                font-size: 1.8rem;
                font-weight: 500;
            }}
            
            .table-container {{
                overflow-x: auto;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 15px;
                overflow: hidden;
            }}
            
            th {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 15px 12px;
                text-align: left;
                font-weight: 500;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            td {{
                padding: 15px 12px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 0.9rem;
            }}
            
            tr:hover {{
                background-color: #f8f9ff;
                transition: background-color 0.3s ease;
            }}
            
            .status-success {{
                color: #27ae60;
                font-weight: 600;
                padding: 4px 12px;
                background: #d5f4e6;
                border-radius: 20px;
                font-size: 0.8rem;
            }}
            
            .status-error {{
                color: #e74c3c;
                font-weight: 600;
                padding: 4px 12px;
                background: #fadbd8;
                border-radius: 20px;
                font-size: 0.8rem;
            }}
            
            .timestamp {{
                font-size: 0.8rem;
                color: #7f8c8d;
                font-family: 'Courier New', monospace;
            }}
            
            .response-content {{
                max-height: 400px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-break: break-all;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 12px;
                line-height: 1.4;
                color: #495057;
            }}
            
            .response-content::-webkit-scrollbar {{
                width: 8px;
            }}
            
            .response-content::-webkit-scrollbar-track {{
                background: #f1f1f1;
                border-radius: 4px;
            }}
            
            .response-content::-webkit-scrollbar-thumb {{
                background: #c1c1c1;
                border-radius: 4px;
            }}
            
            .response-content::-webkit-scrollbar-thumb:hover {{
                background: #a8a8a8;
            }}
            
            .url-cell {{
                max-width: 300px;
                word-break: break-all;
                color: #3498db;
            }}
            
            /* 动画定义 */
            @keyframes fadeInDown {{
                from {{
                    opacity: 0;
                    transform: translateY(-30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
            
            .pulse {{
                animation: pulse 2s infinite;
            }}
            
            /* 响应式设计 */
            @media (max-width: 768px) {{
                .container {{
                    padding: 10px;
                }}
                
                .header h1 {{
                    font-size: 2rem;
                }}
                
                .stats-grid {{
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                }}
                
                .stat-card {{
                    padding: 15px;
                }}
                
                .stat-card h3 {{
                    font-size: 1.5rem;
                }}
                
                th, td {{
                    padding: 10px 8px;
                    font-size: 0.8rem;
                }}
                
                .response-content {{
                    max-height: 200px;
                    font-size: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>API压力测试报告</h1>
                <p>专业性能分析与监控</p>
            </div>
            
            <div class="summary">
                <h2>测试摘要</h2>
                <div class="stats-grid">
                    <div class="stat-card success">
                        <h3>{success}</h3>
                        <p>成功请求</p>
                    </div>
                    <div class="stat-card error">
                        <h3>{error}</h3>
                        <p>失败请求</p>
                    </div>
                    <div class="stat-card info">
                        <h3>{total}</h3>
                        <p>总请求数</p>
                    </div>
                    <div class="stat-card performance">
                        <h3>{qps:.2f}</h3>
                        <p>QPS (req/sec)</p>
                    </div>
                    <div class="stat-card info">
                        <h3>{avg_time:.2f}ms</h3>
                        <p>平均响应时间</p>
                    </div>
                    <div class="stat-card performance">
                        <h3>{min_time:.2f}ms</h3>
                        <p>最快响应</p>
                    </div>
                    <div class="stat-card performance">
                        <h3>{max_time:.2f}ms</h3>
                        <p>最慢响应</p>
                    </div>
                    <div class="stat-card info">
                        <h3>{test_duration}s</h3>
                        <p>测试持续时间</p>
                    </div>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px; border-left: 4px solid #667eea;">
                    <p><strong>测试时间范围:</strong> {start_time.strftime('%Y-%m-%d %H:%M:%S')} 至 {end_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>并发配置:</strong> {concurrent_threads} 线程并发</p>
                </div>
            </div>

            <div class="table-section">
                <h2>请求明细记录</h2>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>时间戳</th>
                                <th>请求URL</th>
                                <th>状态码</th>
                                <th>响应时间</th>
                                <th>状态</th>
                                <th>完整响应内容</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join([f'''
                            <tr style="animation: fadeInUp 0.5s ease-out {i * 0.1}s both;">
                                <td class="timestamp">{row["timestamp"]}</td>
                                <td class="url-cell">{row["url"]}</td>
                                <td>{row["status_code"]}</td>
                                <td>{row["response_time"]}</td>
                                <td><span class="status-{row["status"].lower()}">{row["status"]}</span></td>
                                <td><div class="response-content">{html.escape(row["response_content"])}</div></td>
                            </tr>
                            ''' for i, row in enumerate(requests_data[:500])])}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <script>
            // 添加交互效果
            document.addEventListener('DOMContentLoaded', function() {{
                // 为统计卡片添加点击效果
                const statCards = document.querySelectorAll('.stat-card');
                statCards.forEach(card => {{
                    card.addEventListener('click', function() {{
                        this.style.transform = 'scale(0.95)';
                        setTimeout(() => {{
                            this.style.transform = 'translateY(-5px)';
                        }}, 150);
                    }});
                }});
                
                // 为表格行添加点击高亮效果
                const tableRows = document.querySelectorAll('tbody tr');
                tableRows.forEach(row => {{
                    row.addEventListener('click', function() {{
                        this.style.background = '#e3f2fd';
                        setTimeout(() => {{
                            this.style.background = '';
                        }}, 500);
                    }});
                }});
                
                // 添加滚动动画
                const observerOptions = {{
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                }};
                
                const observer = new IntersectionObserver((entries) => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersecting) {{
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }}
                    }});
                }}, observerOptions);
                
                // 观察所有表格行
                tableRows.forEach(row => {{
                    row.style.opacity = '0';
                    row.style.transform = 'translateY(20px)';
                    row.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    observer.observe(row);
                }});
            }});
        </script>
    </body>
    </html>
    """

    # 写入报告文件（使用UTF-8编码）
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content) 