# 创建结构化输出评估脚本

文件：

```text
evals/scripts/eval_task_extraction.py
```

代码：

```python
import json
from pathlib import Path
from typing import Any

import requests


BASE_URL = "http://localhost:8080"
DATASET_PATH = Path("evals/datasets/task_extraction_cases.jsonl")
REPORT_PATH = Path("evals/reports/task_extraction_failures.jsonl")


def load_cases(path: Path) -> list[dict[str, Any]]:
    """读取 JSONL 测试集。"""
    cases: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            cases.append(json.loads(line))

    return cases


def call_extract_task(text: str) -> dict[str, Any]:
    """调用 Java AI Gateway 的任务抽取接口。"""
    response = requests.post(
        f"{BASE_URL}/api/ai/extract-task",
        json={"text": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def normalize_value(value: Any) -> Any:
    """做轻量规范化，避免因为前后空格导致误判。"""
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    return value


def compare_case(expected: dict[str, Any], actual: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    对比 expected 和 actual。

    当前先做严格字段对比：
    - taskName
    - dueTimeText
    - priority
    - assignee
    """
    errors: list[str] = []

    for field in ["taskName", "dueTimeText", "priority", "assignee"]:
        expected_value = normalize_value(expected.get(field))
        actual_value = normalize_value(actual.get(field))

        if expected_value != actual_value:
            errors.append(
                f"{field}: expected={expected_value!r}, actual={actual_value!r}"
            )

    return len(errors) == 0, errors


def main() -> None:
    """执行结构化输出评估。"""
    cases = load_cases(DATASET_PATH)

    total = len(cases)
    passed = 0
    failures: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["id"]
        text = case["input"]
        expected = case["expected"]

        try:
            actual = call_extract_task(text)
            ok, errors = compare_case(expected, actual)

            if ok:
                passed += 1
                print(f"[PASS] {case_id}")
            else:
                print(f"[FAIL] {case_id}: {errors}")
                failures.append(
                    {
                        "id": case_id,
                        "input": text,
                        "expected": expected,
                        "actual": actual,
                        "errors": errors,
                    }
                )

        except Exception as exc:
            print(f"[ERROR] {case_id}: {exc}")
            failures.append(
                {
                    "id": case_id,
                    "input": text,
                    "expected": expected,
                    "actual": None,
                    "errors": [str(exc)],
                }
            )

    pass_rate = passed / total if total else 0

    print()
    print("=== Task Extraction Eval Result ===")
    print(f"total: {total}")
    print(f"passed: {passed}")
    print(f"failed: {total - passed}")
    print(f"pass_rate: {pass_rate:.2%}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        for failure in failures:
            file.write(json.dumps(failure, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
```
