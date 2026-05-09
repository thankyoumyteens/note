# 新增查询 Controller

新建：

```text
controller/LlmCallLogController.java
```

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.LlmCallLog;
import com.example.aigateway.service.LlmCallLogService;
import java.util.List;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ai")
public class LlmCallLogController {

    private final LlmCallLogService llmCallLogService;

    public LlmCallLogController(LlmCallLogService llmCallLogService) {
        this.llmCallLogService = llmCallLogService;
    }

    @GetMapping("/llm-call-logs")
    public List<LlmCallLog> findRecent() {
        return llmCallLogService.findRecent();
    }
}
```
