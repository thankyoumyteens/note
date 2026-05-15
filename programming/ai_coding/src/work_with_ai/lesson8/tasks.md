# 合格的 tasks.md 应该能指导第 9 课

比如：

```markdown
# Tasks

- [ ] Add `findById(String id)` to `InMemoryDocumentStore`.
- [ ] Add a response DTO for document query if needed.
- [ ] Add `GET /api/documents/{id}` to `DocumentController`.
- [ ] Return `200 OK` with `documentId`, `title`, and `content` when found.
- [ ] Return `404 Not Found` with a simple error response when not found.
- [ ] Add MockMvc tests for successful query.
- [ ] Add MockMvc tests for missing document.
- [ ] Ensure existing create-document tests still pass.
- [ ] Ensure health-check tests still pass.
- [ ] Run `mvn test`.
```
