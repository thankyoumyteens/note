# 第二步 Prompt：只实现内存存储

第一步没问题后，再发：

```text
目标：
继续第 7 课。现在只执行第 2 小步：新增内存文档存储。

本次允许新增：
src/main/java/com/example/aidocsummary/document/InMemoryDocumentStore.java

设计要求：
1. 使用 ConcurrentHashMap<String, Document> 保存文档。
2. 使用 AtomicLong 生成递增字符串 ID，例如 "1"、"2"。
3. 提供 save(String title, String content) 方法，返回 Document。
4. 暂时不提供查询方法。
5. 标记为 Spring Bean，例如使用 @Component。

限制：
1. 不要修改 pom.xml。
2. 不要修改 README.md。
3. 不要实现 Controller。
4. 不要新增测试。
5. 不要接入数据库或新增依赖。
6. 不要实现文档查询接口。
7. 不要修改第一步之外的无关文件。

完成后请输出：
1. 新增/修改了哪些文件
2. save 方法行为
3. 是否修改了无关文件
4. 下一步建议
```

然后再检查：

```bash
git diff --stat
git diff
```
