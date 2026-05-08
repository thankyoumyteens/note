# 新增 Controller 接口

新建或修改：

```text
controller/TaskExtractionController.java
```

代码：

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.TaskExtractionRequest;
import com.example.aigateway.dto.TaskExtractionResult;
import com.example.aigateway.service.TaskExtractionService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ai")
public class TaskExtractionController {

    private final TaskExtractionService taskExtractionService;

    public TaskExtractionController(TaskExtractionService taskExtractionService) {
        this.taskExtractionService = taskExtractionService;
    }

    @PostMapping("/extract-task")
    public TaskExtractionResult extractTask(@RequestBody TaskExtractionRequest request) {
        return taskExtractionService.extract(request.text());
    }
}
```
