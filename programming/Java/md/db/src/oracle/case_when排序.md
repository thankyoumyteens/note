# case when 排序

排序顺序: CHECK_STATUS == 01 && CHECK_TYPE == 02 > CHECK_STATUS == 01 && CHECK_TYPE == 01 > 其它 > UPDATE_TIME desc > CREATE_TIME desc

```sql
select
    *
from
    table1 a
    left join table2 b ON a.id = b.aid
where
    a.STATUS = #{status}
order by
    case
        when CHECK_STATUS = '01'
        and CHECK_TYPE = '02' then 0
        when CHECK_STATUS = '01'
        and CHECK_TYPE = '01' then 1
        else 2
    end,
    UPDATE_TIME desc,
    CREATE_TIME desc
```
