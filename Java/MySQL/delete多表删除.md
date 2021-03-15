# delete多表删除

```sql
DELETE t1,t2 from t1 LEFT JOIN t2 ON t1.id=t2.id WHERE t1.id=25
```
