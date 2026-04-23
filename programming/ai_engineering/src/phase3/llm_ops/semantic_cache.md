# 语义缓存

如果说 Prompt Caching 是大模型在它的大脑里帮你想办法“省力”，那语义缓存就是你在大模型的家门口装了一个智能门卫。这个门卫不看你穿什么衣服（单词拼写），只看你想干什么（语义意图）。

传统的 Java 缓存（比如基于 Spring Cache 或 Guava）只能做精确匹配（Exact Match）。用户问“查订单 ORD-002”和“帮我看看 ORD-002 订单”，在传统哈希表里是两个完全不同的 Key。

但在 AI 时代，架构师会把用户的提问变成**向量（Vector/Embedding）**存进 Redis。下次用户提问时，系统会计算两个向量的余弦相似度（Cosine Similarity）。如果相似度高达 0.95，直接把 Redis 里的旧答案扔给用户。这不仅把 TTFT（首字延迟）从几秒降到了几毫秒，更是在物理层面上省下了大笔的 API 调用费。

底层的“三步走”流程：

1. 向量化 (Embedding)：用户提问进来，先调个便宜的模型（如 text-embedding-3-small）转成一串数字。
2. 相似度检索 (Vector Search)：在 Redis 或向量数据库里找，“谁离这串数字最近？”。
3. 阈值判断 (Thresholding)：如果相似度（Cosine Similarity）大于 0.95，判定为同一件事，直接返回答案。

原生 redis 只能存简单的 Key-Value，它算不了向量（Distance）。在企业级架构中，我们通常直接使用包含了所有高级 Module 的 Redis Stack。
