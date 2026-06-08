# 新增 Tool Eval 脚本

批量创建 ticket、运行 plan step，然后检查 structuredPlan。

本课先做轻量 eval，不做 LLM-as-judge。

### 代码

文件：

```text
python-tools/scripts/eval_tool_plan.py
```

```python
import json
from pathlib import Path
from typing import Any

import httpx


BASE_URL = "http://localhost:8080"
DATASET_PATH = Path("tool_eval_cases.jsonl")


HEADERS = {
    "X-Tenant-Id": "tenant-a",
    "X-User-Id": "tool-eval-user",
    "X-Roles": "support",
    "Content-Type": "application/json",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows


def create_ticket(client: httpx.Client, case: dict[str, Any]) -> str:
    response = client.post(
        "/api/agent/tickets",
        headers=HEADERS,
        json={
            "title": case["title"],
            "description": case["description"],
        },
    )
    response.raise_for_status()
    return response.json()["ticketId"]


def run_once(client: httpx.Client, ticket_id: str) -> dict[str, Any]:
    response = client.post(
        f"/api/agent/tickets/{ticket_id}/run",
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    cases = load_jsonl(DATASET_PATH)

    total = len(cases)
    passed = 0

    with httpx.Client(base_url=BASE_URL, timeout=60.0) as client:
        for case in cases:
            ticket_id = create_ticket(client, case)

            # 第一次 run 只执行 PLAN
            result = run_once(client, ticket_id)

            plan = result.get("structuredPlan") or {}
            tool = plan.get("requiredTool")
            args = plan.get("arguments") or {}
            order_id = args.get("orderId")

            errors = []

            if tool != case["expectedTool"]:
                errors.append(f"expected tool={case['expectedTool']}, actual={tool}")

            if order_id != case["expectedOrderId"]:
                errors.append(f"expected orderId={case['expectedOrderId']}, actual={order_id}")

            if errors:
                print(f"[FAIL] {case['id']}: {errors}")
            else:
                passed += 1
                print(f"[PASS] {case['id']}")

    print()
    print("=== Tool Plan Eval Result ===")
    print(f"total: {total}")
    print(f"passed: {passed}")
    print(f"failed: {total - passed}")
    print(f"pass_rate: {passed / total:.2%}" if total else "pass_rate: 0.00%")


if __name__ == "__main__":
    main()
```

### 注意

为了让 eval 能看到 `structuredPlan`，需要修改 `AgentTicketResponse.java`：

```java
package com.example.aigateway.agent.dto;

import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.agent.model.AgentWorkflowStatus;
import com.example.aigateway.agent.model.AgentWorkflowStep;
import java.util.List;
import java.util.UUID;

public record AgentTicketResponse(
        UUID ticketId,
        String title,
        String description,
        AgentWorkflowStatus status,
        AgentWorkflowStep currentStep,
        int stepCount,
        int toolCallCount,
        String plan,
        AgentPlan structuredPlan,
        String orderCheckResult,
        String draftReply,
        String humanReviewComment,
        String summary,
        List<String> eventLogs
) {
    public static AgentTicketResponse from(AgentTicket ticket) {
        return new AgentTicketResponse(
                ticket.getId(),
                ticket.getTitle(),
                ticket.getDescription(),
                ticket.getStatus(),
                ticket.getCurrentStep(),
                ticket.getStepCount(),
                ticket.getToolCallCount(),
                ticket.getPlan(),
                ticket.getStructuredPlan(),
                ticket.getOrderCheckResult(),
                ticket.getDraftReply(),
                ticket.getHumanReviewComment(),
                ticket.getSummary(),
                ticket.getEventLogs()
        );
    }
}
```
