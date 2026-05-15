# 第四步 Prompt：只新增测试

Controller 实现后，再让 Codex 写测试：

```text
目标：
继续第 7 课。现在只执行第 4 小步：为 POST /api/documents 新增测试。

本次允许新增：
src/test/java/com/example/aidocsummary/document/DocumentControllerTests.java

测试要求：
使用现有 Spring Boot Test / MockMvc，不新增依赖。

必须覆盖：
1. 保存成功：title 和 content 合法，返回 201，响应包含 documentId。
2. title 为空字符串，返回 400。
3. title 为纯空格，返回 400。
4. content 为空字符串，返回 400。
5. content 为纯空格，返回 400。
6. 健康检查接口不受影响。

限制：
1. 不要修改 pom.xml。
2. 不要新增依赖。
3. 不要修改业务代码，除非测试暴露出编译错误，并先说明原因。
4. 不要改变成功响应格式。
5. 不要实现查询接口。
6. 不要实现摘要接口。
7. 不要接入数据库、AI API、用户系统或 Spring Security。

完成后请输出：
1. 新增/修改了哪些文件
2. 测试覆盖哪些场景
3. 是否修改业务代码
4. 下一步应该运行的命令
```
