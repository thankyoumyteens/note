# 新增 Controller 接口

文件：

```text
src/main/java/com/example/aigateway/controller/TaskExtractionController.java
```

代码：

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.TaskExtractionRequest;
import com.example.aigateway.dto.TaskExtractionResult;
import com.example.aigateway.service.TaskExtractionService;
import org.springframework.web.bind.annotation.*;

/**
 * 任务信息抽取接口。
 *
 * 该接口不是普通聊天接口。
 * 它的目标是把自然语言任务描述转换成 Java DTO。
 */
@RestController
@RequestMapping("/api/ai")
public class TaskExtractionController {

    private final TaskExtractionService taskExtractionService;

    public TaskExtractionController(TaskExtractionService taskExtractionService) {
        this.taskExtractionService = taskExtractionService;
    }

    /**
     * 从用户输入中抽取任务信息。
     */
    @PostMapping("/extract-task")
    public TaskExtractionResult extractTask(@RequestBody TaskExtractionRequest request) {
        return taskExtractionService.extract(request.text());
    }
}
```
