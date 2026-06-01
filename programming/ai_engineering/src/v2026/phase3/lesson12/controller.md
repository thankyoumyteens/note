# 新增 Controller

暴露 Spring AI RAG Demo 接口，和第 11 课主线接口区分开。

第 11 课接口：

```http
POST /api/rag/documents
POST /api/rag/query
```

第 12 课接口：

```http
POST /api/spring-ai/rag/documents
POST /api/spring-ai/rag/query
```

路径不同，避免混淆两个实现。

#### 代码

`SpringAiRagDocumentController.java`

```java
package com.example.aigateway.springai.rag.controller;

import com.example.aigateway.springai.rag.dto.SpringAiRagUploadResponse;
import com.example.aigateway.springai.rag.service.SpringAiRagService;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

/**
 * Spring AI RAG 文档接口。
 */
@RestController
@RequestMapping("/api/spring-ai/rag")
public class SpringAiRagDocumentController {

    private final SpringAiRagService springAiRagService;

    public SpringAiRagDocumentController(SpringAiRagService springAiRagService) {
        this.springAiRagService = springAiRagService;
    }

    @PostMapping("/documents")
    public SpringAiRagUploadResponse upload(@RequestParam("file") MultipartFile file) {
        return springAiRagService.upload(file);
    }
}
```

`SpringAiRagQueryController.java`

```java
package com.example.aigateway.springai.rag.controller;

import com.example.aigateway.springai.rag.dto.SpringAiRagQueryRequest;
import com.example.aigateway.springai.rag.dto.SpringAiRagQueryResponse;
import com.example.aigateway.springai.rag.service.SpringAiRagService;
import org.springframework.web.bind.annotation.*;

/**
 * Spring AI RAG 查询接口。
 */
@RestController
@RequestMapping("/api/spring-ai/rag")
public class SpringAiRagQueryController {

    private final SpringAiRagService springAiRagService;

    public SpringAiRagQueryController(SpringAiRagService springAiRagService) {
        this.springAiRagService = springAiRagService;
    }

    @PostMapping("/query")
    public SpringAiRagQueryResponse query(@RequestBody SpringAiRagQueryRequest request) {
        return springAiRagService.query(request);
    }
}
```
