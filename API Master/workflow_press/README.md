# API压力测试工具

这是一个用于API压力测试的工具，支持多种请求体模板的动态选择。

## 功能特性

- 支持多种请求体模板的动态选择
- 实时进度显示
- 详细的统计报告
- HTML报告生成
- 可配置的并发线程数和测试持续时间

## 文件结构

```
workflow_press/
├── workflow_press_test.py      # 主测试文件
├── request_templates.py        # 请求体模板配置文件
├── url_config.py              # URL配置文件
├── html_report_generator.py   # HTML报告生成器
└── README.md                  # 说明文档
```

## 使用方法

1. 运行主测试文件：
   ```bash
   python workflow_press_test.py
   ```

2. 程序会显示可用的请求体模板：
   ```
   可用的请求体模板:
   ------------------------------
   1. image_processing
   2. text_processing
   3. document_processing
   4. multimodal
   ------------------------------
   ```

3. 输入模板名称或编号进行选择：
   ```
   请选择请求体模板 (输入模板名称或编号): 1
   已选择模板: image_processing
   ```

4. 程序会自动开始压力测试并显示实时进度。

## 请求体模板

### 1. image_processing
用于图像处理的API测试，包含文件上传和图像分析功能。

### 2. text_processing
用于文本处理的API测试，包含文本分析和生成功能。

### 3. document_processing
用于文档处理的API测试，支持PDF等文档格式。

### 4. multimodal
用于多模态API测试，同时处理图像和文本输入。

## 添加新的请求体模板

要添加新的请求体模板，请编辑 `request_templates.py` 文件：

1. 定义新的模板：
   ```python
   NEW_TEMPLATE = {
       "inputs": {
           "your_field": None,  # 动态填充
           # ... 其他字段
       },
       "user": "abc-123",
       "response_mode": "streaming"
   }
   ```

2. 将模板添加到 `REQUEST_TEMPLATES` 字典中：
   ```python
   REQUEST_TEMPLATES = {
       "image_processing": IMAGE_PROCESSING_TEMPLATE,
       "text_processing": TEXT_PROCESSING_TEMPLATE,
       "document_processing": DOCUMENT_PROCESSING_TEMPLATE,
       "multimodal": MULTIMODAL_TEMPLATE,
       "new_template": NEW_TEMPLATE  # 添加新模板
   }
   ```

## 配置参数

在 `workflow_press_test.py` 中可以修改以下配置：

- `CONCURRENT_THREADS`: 并发线程数
- `TEST_DURATION`: 测试持续时间（秒）
- `TARGET_URL`: 目标API地址
- `AUTH_TOKEN`: 认证令牌

## 输出文件

测试完成后会生成：
- 控制台统计报告
- HTML格式的详细报告文件

## 注意事项

- 确保 `url_config.py` 中配置了有效的测试URL
- 确保 `AUTH_TOKEN` 已正确设置
- 根据目标API的实际情况调整请求体模板 