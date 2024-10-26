# 锁定用户

```sql
-- 锁定
alter user 用户名@'白名单' account lock;

-- 解锁
alter user 用户名@'白名单' account unlock;
```
