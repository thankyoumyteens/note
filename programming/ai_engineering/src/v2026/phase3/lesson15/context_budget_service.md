# 新增 ContextBudgetService

按预算选择哪些上下文能进入 prompt。

基础策略：

```text
1. 按 priority 从高到低排序
2. 在预算内尽量保留
3. 超预算的丢弃
4. 返回 selected / dropped
```

这叫 context packing。

### 代码

文件：

```text
src/main/java/com/example/aigateway/context/service/ContextBudgetService.java
```

```java
package com.example.aigateway.context.service;

import com.example.aigateway.context.config.ContextProperties;
import com.example.aigateway.context.dto.ContextBudget;
import com.example.aigateway.context.dto.ContextItem;
import com.example.aigateway.context.dto.ContextPackResult;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * 上下文预算服务。
 *
 * 负责从候选上下文中挑选能进入 prompt 的部分。
 */
@Service
public class ContextBudgetService {

    private final ContextProperties properties;

    public ContextBudgetService(ContextProperties properties) {
        this.properties = properties;
    }

    public ContextBudget ragBudget() {
        int maxContextTokens = Math.min(
                properties.getMaxInputTokens() - properties.getReservedOutputTokens(),
                properties.getMaxRagContextTokens()
        );

        return new ContextBudget(
                properties.getMaxInputTokens(),
                properties.getReservedOutputTokens(),
                maxContextTokens
        );
    }

    public ContextPackResult pack(
            List<ContextItem> candidates,
            ContextBudget budget
    ) {
        List<ContextItem> sorted = candidates.stream()
                .sorted(Comparator.comparingInt(ContextItem::priority).reversed())
                .toList();

        List<ContextItem> selected = new ArrayList<>();
        List<ContextItem> dropped = new ArrayList<>();

        int total = 0;

        for (ContextItem item : sorted) {
            if (total + item.tokenCount() <= budget.maxContextTokens()) {
                selected.add(item);
                total += item.tokenCount();
            } else {
                dropped.add(item);
            }
        }

        return new ContextPackResult(
                selected,
                dropped,
                total,
                !dropped.isEmpty()
        );
    }
}
```

### 代码说明

这个版本不做复杂优化，只做最清晰的优先级选择。

后续可以加入：

```text
按 score 排序
按 citation 保留
按 recency 保留
按 role 保留
压缩后再尝试放入
```
