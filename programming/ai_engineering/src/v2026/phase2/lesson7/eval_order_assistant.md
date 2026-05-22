# 创建订单助手评估脚本

文件：

```text
evals/scripts/eval_order_assistant.py
```

代码：

```python
import json
from pathlib import Path
from typing import Any

import requests


BASE_URL = "http://localhost:8080"
DATASET_PATH = Path("evals/datasets/order_assistant_cases.jsonl")
REPORT_PATH = Path("evals/reports/order_assistant_failures.jsonl")


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


def call_order_assistant(message: str) -> dict[str, Any]:
    """调用 Java AI Gateway 的订单助手接口。"""
    response = requests.post(
        f"{BASE_URL}/api/ai/order-assistant",
        json={"message": message},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def compare_case(expected: dict[str, Any], actual: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    对比订单助手输出。

    当前接口只返回 answer，所以先判断 answer 是否包含关键文本。
    """
    errors: list[str] = []

    answer = actual.get("answer")
    should_contain = expected.get("shouldContain")

    if not isinstance(answer, str):
        errors.append(f"answer is not string: {answer!r}")
        return False, errors

    if should_contain not in answer:
        errors.append(
            f"answer should contain {should_contain!r}, actual={answer!r}"
        )

    return len(errors) == 0, errors


def main() -> None:
    """执行订单助手评估。"""
    cases = load_cases(DATASET_PATH)

    total = len(cases)
    passed = 0
    failures: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["id"]
        message = case["input"]
        expected = case["expected"]

        try:
            actual = call_order_assistant(message)
            ok, errors = compare_case(expected, actual)

            if ok:
                passed += 1
                print(f"[PASS] {case_id}")
            else:
                print(f"[FAIL] {case_id}: {errors}")
                failures.append(
                    {
                        "id": case_id,
                        "input": message,
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
                    "input": message,
                    "expected": expected,
                    "actual": None,
                    "errors": [str(exc)],
                }
            )

    pass_rate = passed / total if total else 0

    print()
    print("=== Order Assistant Eval Result ===")
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
