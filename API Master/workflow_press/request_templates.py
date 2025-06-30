# 请求体模板配置文件
# 包含各种API测试场景的请求体模板

# 基础图像处理请求模板
IMAGE_PROCESSING_TEMPLATE = {
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

# 文本处理请求模板
TEXT_PROCESSING_TEMPLATE = {
    "inputs": {
        "text": None,  # 动态填充
        "prompt": "请分析以下文本内容",
        "max_tokens": 1000
    },
    "user": "abc-123",
    "response_mode": "streaming"
}

# 文档处理请求模板
DOCUMENT_PROCESSING_TEMPLATE = {
    "inputs": {
        "document": None,  # 动态填充
        "document_type": "pdf",
        "extraction_mode": "full"
    },
    "user": "abc-123",
    "response_mode": "streaming"
}

# 多模态请求模板
MULTIMODAL_TEMPLATE = {
    "inputs": {
        "image": None,  # 动态填充
        "text": None,   # 动态填充
        "task": "image_caption"
    },
    "user": "abc-123",
    "response_mode": "streaming"
}

# 所有可用的请求体模板
REQUEST_TEMPLATES = {
    "image_processing": IMAGE_PROCESSING_TEMPLATE,
    "text_processing": TEXT_PROCESSING_TEMPLATE,
    "document_processing": DOCUMENT_PROCESSING_TEMPLATE,
    "multimodal": MULTIMODAL_TEMPLATE
}

def get_template(template_name):
    """
    根据模板名称获取请求体模板
    
    Args:
        template_name (str): 模板名称
        
    Returns:
        dict: 请求体模板的副本
    """
    if template_name not in REQUEST_TEMPLATES:
        raise ValueError(f"未知的模板名称: {template_name}. 可用模板: {list(REQUEST_TEMPLATES.keys())}")
    
    # 返回模板的深拷贝，避免修改原始模板
    import copy
    return copy.deepcopy(REQUEST_TEMPLATES[template_name])

def list_available_templates():
    """
    列出所有可用的模板
    
    Returns:
        list: 模板名称列表
    """
    return list(REQUEST_TEMPLATES.keys())

def print_available_templates():
    """
    打印所有可用的模板信息
    """
    print("可用的请求体模板:")
    print("-" * 30)
    for i, template_name in enumerate(REQUEST_TEMPLATES.keys(), 1):
        print(f"{i}. {template_name}")
    print("-" * 30) 