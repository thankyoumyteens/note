# 重试和降级

项目结构

```
agent-dev-py
├── .env
├── pyproject.toml
└── src
    └── llm_api_demo
        ├── __init__.py
        ├── settings.py
        ├── schemas.py
        ├── exceptions.py
        ├── provider_clients.py
        ├── fallback_router.py
        └── main.py
```
