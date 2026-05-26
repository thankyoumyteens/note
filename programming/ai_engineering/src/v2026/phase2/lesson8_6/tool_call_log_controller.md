# 修改 ToolCallLogController

让工具调用日志支持按 `toolName / success / traceId` 查询。

这会为后续白盒 eval 提供基础。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/controller/ToolCallLogController.java
```

替换为：

```java
package com.example.aigateway.controller;

import com.example.aigateway.entity.ToolCallLogEntity;
import com.example.aigateway.service.ToolCallLogService;
import java.util.List;
import org.springframework.web.bind.annotation.*;

/**
 * 工具调用日志查询接口。
 *
 * 当前用于 eval 调试。
 * 生产环境必须增加权限控制。
 */
@RestController
@RequestMapping("/api/ai")
public class ToolCallLogController {

    private final ToolCallLogService toolCallLogService;

    public ToolCallLogController(ToolCallLogService toolCallLogService) {
        this.toolCallLogService = toolCallLogService;
    }

    @GetMapping("/tool-call-logs")
    public List<ToolCallLogEntity> logs(
            @RequestParam(required = false) String toolName,
            @RequestParam(required = false) Boolean success,
            @RequestParam(required = false) String traceId
    ) {
        if (toolName != null && !toolName.isBlank()) {
            return toolCallLogService.findByToolName(toolName);
        }

        if (success != null) {
            return toolCallLogService.findBySuccess(success);
        }

        if (traceId != null && !traceId.isBlank()) {
            return toolCallLogService.findByTraceId(traceId);
        }

        return toolCallLogService.recentLogs();
    }
}
```

#### 代码说明

支持：

```http
GET /api/ai/tool-call-logs
GET /api/ai/tool-call-logs?toolName=getOrderStatus
GET /api/ai/tool-call-logs?success=true
GET /api/ai/tool-call-logs?traceId=xxx
```
