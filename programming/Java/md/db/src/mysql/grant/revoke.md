# 收回权限

```sql
revoke 权限 on 权限级别 from 用户;

-- 比如
revoke delete on *.* from test@'%';
```
