# 创建 RAG eval 脚本

批量调用 `/api/rag/query`，输出通过率和失败样本。

第 7 课已经做过 eval。第 13 课把 eval 扩展到 RAG。

#### 代码

文件：

```text
python-tools/scripts/eval_rag_basic.py
```

```python
import json
from pathlib import Path
from typing import Any

import httpx


BASE_URL = "http://localhost:8080"
DATASET_PATH = Path("rag_eval_cases.jsonl")
REPORT_PATH = Path("rag_eval_failures.jsonl")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    return rows


def call_rag(question: str) -> dict[str, Any]:
    with httpx.Client(base_url=BASE_URL, timeout=60.0) as client:
        response = client.post(
            "/api/rag/query",
            json={
                "question": question,
                "topK": 5,
            },
        )
        response.raise_for_status()
        return response.json()


def evaluate_case(case: dict[str, Any], actual: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []

    answer = actual.get("answer") or ""
    chunks = actual.get("chunks") or []
    has_enough_context = actual.get("hasEnoughContext")

    expected_answer_contains = case["expectedAnswerContains"]
    should_have_answer = case["shouldHaveAnswer"]

    if expected_answer_contains not in answer:
        errors.append(
            f"answer should contain {expected_answer_contains!r}, actual={answer!r}"
        )

    if should_have_answer and not chunks:
        errors.append("expected chunks, but got empty chunks")

    if not should_have_answer and has_enough_context is True:
        errors.append("expected no-answer, but hasEnoughContext=true")

    return len(errors) == 0, errors


def main() -> None:
    cases = load_jsonl(DATASET_PATH)

    total = len(cases)
    passed = 0
    failures: list[dict[str, Any]] = []

    for case in cases:
        case_id = case["id"]

        try:
            actual = call_rag(case["question"])
            ok, errors = evaluate_case(case, actual)

            if ok:
                passed += 1
                print(f"[PASS] {case_id}")
            else:
                print(f"[FAIL] {case_id}: {errors}")
                failures.append(
                    {
                        "id": case_id,
                        "question": case["question"],
                        "expected": case,
                        "actual": actual,
                        "errors": errors,
                    }
                )

        except Exception as exc:
            print(f"[ERROR] {case_id}: {exc}")
            failures.append(
                {
                    "id": case_id,
                    "question": case["question"],
                    "expected": case,
                    "actual": None,
                    "errors": [str(exc)],
                }
            )

    pass_rate = passed / total if total else 0

    print()
    print("=== RAG Eval Result ===")
    print(f"total: {total}")
    print(f"passed: {passed}")
    print(f"failed: {total - passed}")
    print(f"pass_rate: {pass_rate:.2%}")

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        for failure in failures:
            file.write(json.dumps(failure, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
```
