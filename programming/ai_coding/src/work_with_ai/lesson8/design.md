# 合格的 design.md 应该包含什么

重点是说明当前系统与拟议变化：

````markdown
# Design

## Current System

- Documents can be created through `POST /api/documents`.
- Documents are stored in memory.
- The create endpoint returns only `documentId`.

## Proposed Changes

- Add a read path to retrieve a document by ID.
- Add a method to the in-memory store, such as `findById(String id)`.
- Add a GET endpoint in `DocumentController`.

## Affected Files

Expected changes for the next lesson:

- `InMemoryDocumentStore.java`
- `DocumentController.java`
- `DocumentControllerTests.java`

Files not expected to change:

- `pom.xml`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- existing create response DTO, unless required by implementation

## Data/API Changes

Request:

`GET /api/documents/{id}`

Success response:

```json
{
  "documentId": "1",
  "title": "Spring Boot 学习笔记",
  "content": "这是一篇文档正文。"
}
```

Not found response:

```json
{
  "error": "document not found"
}
```

## Risks

- In-memory data is lost after application restart.
- Tests must create a document before querying it.
- Do not accidentally change the create endpoint response.
````
