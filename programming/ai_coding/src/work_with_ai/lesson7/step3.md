# 第三步 Prompt：只实现 Controller

第二步没问题后，再发：

```text
目标：
继续第 7 课。现在只执行第 3 小步：实现 POST /api/documents 控制器。

本次允许新增：
src/main/java/com/example/aidocsummary/document/DocumentController.java

接口要求：
1. POST /api/documents
2. 请求 JSON 包含 title、content。
3. title 为 null、空字符串或纯空格时，返回 400。
4. content 为 null、空字符串或纯空格时，返回 400。
5. 保存成功返回 201 Created。
6. 成功响应只返回 documentId。
7. 错误响应可以保持简单，例如 {"error":"title must not be blank"}。

实现要求：
1. 调用 InMemoryDocumentStore.save(title, content)。
2. 可以 trim title 和 content。
3. 不使用 Bean Validation，因为当前不新增依赖。
4. 不实现查询接口。
5. 不实现摘要接口。

限制：
1. 不要修改 pom.xml。
2. 不要新增依赖。
3. 不要接入数据库。
4. 不要接入 AI API。
5. 不要加入 Spring Security。
6. 不要修改 README.md。
7. 不要让成功响应返回 title 或 content。
8. 不要新增测试，本步只实现 Controller。

完成后请输出：
1. 新增/修改了哪些文件
2. 接口行为摘要
3. 参数校验规则
4. 是否修改了无关文件
5. 下一步建议
```

检查重点：

```text
成功响应只包含 documentId
不要返回 content
不要加依赖
不要改 pom.xml
```
