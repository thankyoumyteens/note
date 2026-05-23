# 新增 LlmCallLogController

文件：

```text
src/main/java/com/example/aigateway/controller/LlmCallLogController.java
```

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.LlmCallLog;
import com.example.aigateway.service.LlmCallLogService;
import java.util.List;
import org.springframework.web.bind.annotation.*;

/**
 * 大模型调用日志查询接口。
 *
 * 当前用于学习和调试。
 * 生产环境需要加权限控制，避免暴露内部调用信息。
 */
@RestController
@RequestMapping("/api/ai")
public class LlmCallLogController {

    private final LlmCallLogService llmCallLogService;

    public LlmCallLogController(LlmCallLogService llmCallLogService) {
        this.llmCallLogService = llmCallLogService;
    }

    @GetMapping("/llm-call-logs")
    public List<LlmCallLog> recentLogs() {
        return llmCallLogService.recentLogs();
    }
}
```
