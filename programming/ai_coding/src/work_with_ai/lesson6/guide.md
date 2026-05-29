# 不符合预期怎么纠正

## 如果计划过度设计，怎么纠正

如果 Claude Code 提到：

```text
JPA
Repository
Entity
H2
PostgreSQL
Spring Security
Spring AI
OpenAI API
Swagger
全局异常框架
文件上传
用户系统
```

发这个：

```text
当前计划过度设计。第 6 课只允许为内存版 POST /api/documents 制定实现计划。

请去掉：
1. 数据库、JPA、Repository、Entity、H2、PostgreSQL、MySQL、Redis
2. Spring Security
3. Spring AI
4. 真实 AI API
5. 用户系统
6. 文件上传
7. 查询接口
8. 摘要接口
9. 新依赖
10. 复杂全局异常体系

请重新输出 7 个 Markdown 章节。
成功响应只返回 documentId。
不要修改任何项目文件。
```

---

## 如果它直接改代码，怎么纠正

发这个：

```text
本课是第 6 课：先计划，后执行，只允许输出实现计划，不允许修改代码或创建文件。

请停止修改文件。
请确认本次是否已经修改任何文件。
如果已修改，请说明修改了哪些文件，并给出回退建议。

然后重新只输出 7 个 Markdown 章节：
1. 需求理解
2. 涉及文件
3. 修改步骤
4. 数据结构 / API 变化
5. 测试计划
6. 风险和回滚方式
7. 计划自检
```

---

## 如果它把 `content` 放进成功响应

发这个：

```text
成功响应设计不符合第 4～5 课约束。

请把成功响应收敛为只返回 documentId，不返回 title 或 content。
重新输出第 4 节“数据结构 / API 变化”和第 7 节“计划自检”。
```
