# 新增 Repository

保存和读取工单。

本课重点是 Agent Workflow，不是数据库建模。所以先用内存 repository。

注意：这不是生产最终方案。

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/repository/AgentTicketRepository.java
```

```java
package com.example.aigateway.agent.repository;

import com.example.aigateway.agent.model.AgentTicket;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Repository;

/**
 * Agent 工单仓储。
 *
 * 第 16 课先使用内存存储，重点放在 workflow。
 * 后续生产化可切换为数据库。
 */
@Repository
public class AgentTicketRepository {

    private final Map<UUID, AgentTicket> store = new ConcurrentHashMap<>();

    public AgentTicket save(AgentTicket ticket) {
        store.put(ticket.getId(), ticket);
        return ticket;
    }

    public Optional<AgentTicket> findById(UUID id) {
        return Optional.ofNullable(store.get(id));
    }
}
```

### 代码说明

这里用 `ConcurrentHashMap` 是为了本地课程简单可运行。
