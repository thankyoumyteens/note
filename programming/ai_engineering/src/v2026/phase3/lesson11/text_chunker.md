# 新增 TextChunker

把长文档切成多个 chunk。

Chunking 是 RAG 的关键步骤之一。

本课先做简单字符切分：

```text
chunkSize = 800
overlap = 100
```

overlap 的作用是避免句子被切断后上下文丢失。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/service/TextChunker.java
```

```java
package com.example.aigateway.rag.service;

import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * 简单文本切分器。
 *
 * 第 11 课先用字符切分。
 * 后续第 13 课再优化 semantic chunking。
 */
@Service
public class TextChunker {

    // 每个 chunk 最大 800 个字符
    private static final int CHUNK_SIZE = 800;
    // 相邻两个 chunk 重叠 100 个字符
    private static final int OVERLAP = 100;

    public List<String> chunk(String text) {
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("text cannot be empty");
        }

        String normalized = text.strip();

        List<String> chunks = new ArrayList<>();

        int start = 0;

        while (start < normalized.length()) {
            int end = Math.min(start + CHUNK_SIZE, normalized.length());

            String chunk = normalized.substring(start, end).strip();

            if (!chunk.isEmpty()) {
                chunks.add(chunk);
            }

            if (end == normalized.length()) {
                break;
            }

            // 下一段 chunk 不从 end 开始，而是往回退 100 个字符开始
            start = Math.max(0, end - OVERLAP);
        }

        return chunks;
    }
}
```
