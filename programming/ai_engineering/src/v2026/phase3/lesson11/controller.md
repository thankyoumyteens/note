# 新增 Controller

暴露上传文档和 RAG 查询接口。

RAG 有两个入口：

```text
文档入口：上传和入库
查询入口：问题和检索问答
```

这两个入口不要混在一个方法里。

#### 代码

`RagDocumentController.java`

```java
package com.example.aigateway.rag.controller;

import com.example.aigateway.rag.dto.RagUploadResponse;
import com.example.aigateway.rag.service.RagIngestionService;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/rag")
public class RagDocumentController {

    private final RagIngestionService ragIngestionService;

    public RagDocumentController(RagIngestionService ragIngestionService) {
        this.ragIngestionService = ragIngestionService;
    }

    @PostMapping("/documents")
    public RagUploadResponse upload(@RequestParam("file") MultipartFile file) {
        return ragIngestionService.upload(file);
    }
}
```

`RagQueryController.java`

```java
package com.example.aigateway.rag.controller;

import com.example.aigateway.rag.dto.RagQueryRequest;
import com.example.aigateway.rag.dto.RagQueryResponse;
import com.example.aigateway.rag.service.RagQueryService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/rag")
public class RagQueryController {

    private final RagQueryService ragQueryService;

    public RagQueryController(RagQueryService ragQueryService) {
        this.ragQueryService = ragQueryService;
    }

    @PostMapping("/query")
    public RagQueryResponse query(@RequestBody RagQueryRequest request) {
        return ragQueryService.query(request);
    }
}
```
