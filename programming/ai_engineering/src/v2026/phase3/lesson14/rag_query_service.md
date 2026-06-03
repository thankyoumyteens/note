# 修改 RagQueryService

查询时用当前用户身份做权限过滤。

RAG 查询时不能只看问题，还必须看：

```text
当前用户是谁
属于哪个租户
有哪些角色
```

#### 代码

把第 13 课中的：

```java
List<RagRetrievedChunk> rawChunks = chunkRepository.hybridSearch(
        questionEmbedding,
        rewrittenQuestion,
        topK,
        ragProperties.getVectorWeight(),
        ragProperties.getKeywordWeight()
);
```

替换为：

```java
CurrentUserContext currentUser = CurrentUserContextHolder.getRequired();

List<RagRetrievedChunk> rawChunks = chunkRepository.hybridSearchWithPermission(
        questionEmbedding,
        rewrittenQuestion,
        topK,
        ragProperties.getVectorWeight(),
        ragProperties.getKeywordWeight(),
        currentUser.tenantId(),
        currentUser.userId(),
        currentUser.roles()
);
```

需要 import：

```java
import com.example.aigateway.security.CurrentUserContext;
import com.example.aigateway.security.CurrentUserContextHolder;
```
