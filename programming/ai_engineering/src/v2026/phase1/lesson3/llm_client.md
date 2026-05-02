# 修改 LlmClient 接口

现在你的 `LlmClient` 应该是这样：

```java
package com.example.aigateway.client;

public interface LlmClient {

    String chat(String message);
}
```

改成：

```java
package com.example.aigateway.client;

import reactor.core.publisher.Flux;

public interface LlmClient {

    String chat(String message);

    Flux<String> streamChat(String message);
}
```

这里增加了：

```java
Flux<String> streamChat(String message);
```

`Flux<String>` 表示：后端会不断发出一段一段文本。
