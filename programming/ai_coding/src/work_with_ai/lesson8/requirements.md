# 合格的 requirements.md 应该长什么样

它不需要很长，大概这样即可：

```markdown
# Requirements

## Goal

Add a document query endpoint:

`GET /api/documents/{id}`

The endpoint returns a previously saved document by `documentId`.

## User Story

As a user, after creating a document, I want to retrieve it by `documentId` so that I can view the stored title and content.

## Scope

- Add `GET /api/documents/{id}`.
- Return `200 OK` when the document exists.
- Return `404 Not Found` when the document does not exist.
- Continue using in-memory storage.
- Reuse the document data saved by `POST /api/documents`.

## Non-goals

- No database.
- No AI summary generation.
- No external AI API.
- No authentication or authorization.
- No Spring Security.
- No list endpoint.
- No pagination.
- No file upload.
- No dependency changes.
- Do not change `POST /api/documents` response format.

## Acceptance Criteria

- `GET /api/documents/{id}` returns `documentId`, `title`, and `content` for an existing document.
- Missing document returns `404 Not Found`.
- Error response is simple and predictable.
- Existing `POST /api/documents` tests continue to pass.
- Existing health check tests continue to pass.
```
