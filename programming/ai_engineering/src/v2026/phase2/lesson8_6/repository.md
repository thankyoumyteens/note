# 新增 Repository

提供数据库读写能力。

Spring Data JPA 的 Repository 可以自动生成基础 CRUD 方法。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/repository/LlmCallLogRepository.java
```

代码：

```java
package com.example.aigateway.repository;

import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.entity.LlmCallLogEntity;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LlmCallLogRepository extends JpaRepository<LlmCallLogEntity, Long> {

    List<LlmCallLogEntity> findTop100ByOrderByCreatedAtDesc();

    List<LlmCallLogEntity> findTop100ByCallTypeOrderByCreatedAtDesc(LlmCallType callType);

    List<LlmCallLogEntity> findTop100ByModelOrderByCreatedAtDesc(String model);

    List<LlmCallLogEntity> findTop100BySuccessOrderByCreatedAtDesc(boolean success);

    List<LlmCallLogEntity> findTop100ByTraceIdOrderByCreatedAtDesc(String traceId);
}
```

文件：

```text
src/main/java/com/example/aigateway/repository/ToolCallLogRepository.java
```

代码：

```java
package com.example.aigateway.repository;

import com.example.aigateway.entity.ToolCallLogEntity;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ToolCallLogRepository extends JpaRepository<ToolCallLogEntity, Long> {

    List<ToolCallLogEntity> findTop100ByOrderByCreatedAtDesc();

    List<ToolCallLogEntity> findTop100ByToolNameOrderByCreatedAtDesc(String toolName);

    List<ToolCallLogEntity> findTop100BySuccessOrderByCreatedAtDesc(boolean success);

    List<ToolCallLogEntity> findTop100ByTraceIdOrderByCreatedAtDesc(String traceId);
}
```

#### 代码说明

这些方法名是 Spring Data JPA 约定式查询。

例如：

```text
findTop100ByOrderByCreatedAtDesc
```

表示：

```text
按 createdAt 倒序查最近 100 条
```
