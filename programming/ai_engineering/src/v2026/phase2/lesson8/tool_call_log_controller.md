# 新增 ToolCallLogController

文件：

```text
src/main/java/com/example/aigateway/controller/ToolCallLogController.java
```

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.ToolCallLog;
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
    public List<ToolCallLog> recentLogs() {
        return toolCallLogService.recentLogs();
    }
}
```
