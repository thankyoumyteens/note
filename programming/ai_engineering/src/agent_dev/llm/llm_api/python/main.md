# main.py

```python
from __future__ import annotations

from llm_api_demo.clients import LlmProvider, LlmRouter


def main() -> None:
    router = LlmRouter()

    result = router.chat(
        provider=LlmProvider.OPENAI,
        message="用三句话解释 RAG 是什么。",
    )

    print(f"[{result.provider} / {result.model}]")
    print(result.content)


if __name__ == "__main__":
    main()
```

运行：

```bash
uv run python -m llm_api_demo.main
```
