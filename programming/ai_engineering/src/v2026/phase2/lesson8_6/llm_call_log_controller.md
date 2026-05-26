# 修改 LlmCallLogController

让日志查询接口支持基础过滤和统计。

当前接口用于学习和调试，生产环境必须加权限控制。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/controller/LlmCallLogController.java
```

替换为：

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.LlmCallStats;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.entity.LlmCallLogEntity;
import com.example.aigateway.service.LlmCallLogService;
import java.util.List;
import org.springframework.web.bind.annotation.*;

/**
 * 大模型调用日志查询接口。
 *
 * 当前用于学习和调试。
 * 生产环境需要加权限控制。
 */
@RestController
@RequestMapping("/api/ai")
public class LlmCallLogController {

    private final LlmCallLogService llmCallLogService;

    public LlmCallLogController(LlmCallLogService llmCallLogService) {
        this.llmCallLogService = llmCallLogService;
    }

    @GetMapping("/llm-call-logs")
    public List<LlmCallLogEntity> logs(
            @RequestParam(required = false) LlmCallType callType,
            @RequestParam(required = false) String model,
            @RequestParam(required = false) Boolean success,
            @RequestParam(required = false) String traceId
    ) {
        if (callType != null) {
            return llmCallLogService.findByCallType(callType);
        }

        if (model != null && !model.isBlank()) {
            return llmCallLogService.findByModel(model);
        }

        if (success != null) {
            return llmCallLogService.findBySuccess(success);
        }

        if (traceId != null && !traceId.isBlank()) {
            return llmCallLogService.findByTraceId(traceId);
        }

        return llmCallLogService.recentLogs();
    }

    @GetMapping("/llm-call-stats")
    public LlmCallStats stats() {
        return llmCallLogService.stats();
    }
}
```

#### 代码说明

支持查询：

```http
GET /api/ai/llm-call-logs
GET /api/ai/llm-call-logs?callType=CHAT
GET /api/ai/llm-call-logs?model=gpt-4o-mini
GET /api/ai/llm-call-logs?success=true
GET /api/ai/llm-call-logs?traceId=xxx
GET /api/ai/llm-call-stats
```
