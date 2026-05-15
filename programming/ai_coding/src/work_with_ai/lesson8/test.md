# 合格的 test.md 应该覆盖什么

至少覆盖：

````markdown
# Test Plan

## Unit Tests

- In-memory store can find an existing document by ID.
- In-memory store returns empty / null / equivalent result when ID does not exist.

## Integration Tests

- Create a document, then query it by ID.
- Query a missing document ID and expect `404 Not Found`.
- Existing `POST /api/documents` tests still pass.
- Existing `GET /api/health` test still passes.

## Manual Checks

```bash
curl -X POST http://localhost:8080/api/documents \
  -H "Content-Type: application/json" \
  -d '{"title":"Demo","content":"Hello"}'

curl http://localhost:8080/api/documents/1
```

## Regression Risks

- Accidentally changing `POST /api/documents` response format.
- Returning `content` from create endpoint instead of only `documentId`.
- Adding database or dependency changes too early.
- Tests relying on fixed IDs across shared application state.
````
