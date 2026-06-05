# 新增 TokenEstimator

提供一个简单 token 估算器。

不同模型 tokenizer 不一样。精确 token 统计要依赖具体 tokenizer。

但在工程上，早期可以先用粗略估算：

```text
中文：大约 1 个字符 ≈ 1 token
英文：大约 4 个字符 ≈ 1 token
混合文本：用字符数 / 2 做粗估
```

第 15 课不引入复杂 tokenizer，先建立接口，后续可替换。

### 代码

文件：

```text
src/main/java/com/example/aigateway/context/service/TokenEstimator.java
```

```java
package com.example.aigateway.context.service;

import org.springframework.stereotype.Service;

/**
 * Token 估算器。
 *
 * 注意：
 * - 这是粗略估算，不是精确 tokenizer。
 * - 目的是让系统具备上下文预算意识。
 * - 后续可以替换为模型专用 tokenizer。
 */
@Service
public class TokenEstimator {

    /**
     * 估算文本 token 数。
     */
    public int estimate(String text) {
        if (text == null || text.isBlank()) {
            return 0;
        }

        String normalized = text.strip();

        int chineseChars = 0;
        int nonChineseChars = 0;

        for (int i = 0; i < normalized.length(); i++) {
            char c = normalized.charAt(i);

            if (isCjk(c)) {
                chineseChars++;
            } else {
                nonChineseChars++;
            }
        }

        // 中文粗略按 1 char = 1 token
        // 非中文粗略按 4 chars = 1 token
        return chineseChars + (int) Math.ceil(nonChineseChars / 4.0);
    }

    private boolean isCjk(char c) {
        return Character.UnicodeScript.of(c) == Character.UnicodeScript.HAN;
    }
}
```

### 代码说明

这个类的核心价值不是“精确”，而是让后续服务都能问：

```text
这段内容大概占多少 token？
还能不能塞进 prompt？
```
