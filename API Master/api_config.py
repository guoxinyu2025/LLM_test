# api_config.py
api_requests = [
    {
        "name": "OpenAI-chat",
        "url": "https://platform.llmprovider.ai/v1/chat/completions",
        "headers": {
            'Content-Type': 'application/json',
            'Authorization': f''
        },
        "data": {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "给我讲一个短故事，20字左右"}
            ],
            "max_tokens": 500,
            "temperature": 0,
            "n": 1,
            "reasoning_effort": ""
        }
    },
    {
        "name": "OpenAI-completions",
        "url": "https://platform.llmprovider.ai/v1/completions",
        "headers": {
            'Content-Type': 'application/json',
            'Authorization': f''
        },
        "data": {
            "model": "gpt-3.5-turbo-instruct",
            "prompt": "Say this is a test",
            "max_tokens": 7,
            "temperature": 0,
            "n": 3
        }
    },
    {
        "name": "OpenAI-embeddings",
        "url": "https://platform.llmprovider.ai/v1/embeddings",
        "headers": {
            'Content-Type': 'application/json',
            'Authorization': f''
        },
        "data": {
            "model": "text-embedding-ada-002",
            "input": "The quick brown fox jumps over the lazy dog.",
            "user": "user-1234"
        }
    },
    {
        "name": "OpenAI-speech",
        "url": "https://platform.llmprovider.ai/v1/audio/speech",
        "headers": {
            'Content-Type': 'application/json',
            'Authorization': f''
        },
        "data": {
            "model": "tts-1",
            "input": "Hello, how are you today?",
            "voice": "alloy",
            "response_format": "mp3",
            "speed": 1.0
        }
    },
    {
        "name": "OpenAI-Transcription",
        "url": "https://platform.llmprovider.ai/v1/audio/transcriptions",
        "headers": {
            'Authorization': f''
        },
        "files": {
            'file': open('C:/guoxinyu.vendor/桌面/17.mp3', 'rb'),
            'timestamp_granularities[]': ("", "segment"),
            'model': ("", "whisper-1"),
            'response_format': ("", "verbose_json")
        }
    },
    {
        "name": "OpenAI-Image",
        "url": "https://platform.llmprovider.ai/v1/images/generations",
        "headers": {
            'Content-Type': 'application/json',
            'Authorization': f'',
        "data": {
            "model": "dall-e-3",
            "prompt": "A cute baby sea otter",
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
        },
        }
    }

]
