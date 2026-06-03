# 测试方式

### 启动服务

```bash
mvn spring-boot:run
```

---

### 准备文档

```bash
cat > finance-policy.txt <<'EOF'
财务报销规则：员工需要在费用发生后 30 天内提交发票和审批单。
超过 30 天的报销申请需要部门负责人额外审批。
EOF
```

---

### 上传 ROLE 文档

```bash
curl -X POST http://localhost:8080/api/rag/documents \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: finance-owner" \
  -H "X-Roles: finance" \
  -F "file=@finance-policy.txt" \
  -F "visibility=ROLE" \
  -F "allowedRoles=finance"
```

预期：上传成功。

---

### finance 用户可以查到

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-finance-001" \
  -H "X-Roles: finance" \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"报销需要多少天内提交？","topK":3}'
```

预期：

```text
能回答 30 天内提交。
chunks 不为空。
hasEnoughContext = true。
```

---

### engineering 用户查不到

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-eng-001" \
  -H "X-Roles: engineering" \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"报销需要多少天内提交？","topK":3}'
```

预期：

```json
{
  "answer": "根据已提供文档无法确定。",
  "chunks": [],
  "hasEnoughContext": false
}
```

---

### 其它租户查不到

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "X-Tenant-Id: tenant-b" \
  -H "X-User-Id: user-finance-002" \
  -H "X-Roles: finance" \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"报销需要多少天内提交？","topK":3}'
```

预期：查不到。

即使角色是 `finance`，但租户不同，也不能访问。

---

### 测试 PRIVATE

上传：

```bash
curl -X POST http://localhost:8080/api/rag/documents \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: private-owner" \
  -H "X-Roles: employee" \
  -F "file=@finance-policy.txt" \
  -F "visibility=PRIVATE"
```

同一个 owner 可以查到：

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: private-owner" \
  -H "X-Roles: employee" \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"报销需要多少天内提交？","topK":3}'
```

其它用户查不到：

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: other-user" \
  -H "X-Roles: employee" \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"报销需要多少天内提交？","topK":3}'
```
