# explain

```
explain xxxxsql
```

# type列

从最好到最差依次是: system>const>eq_ref>ref>range>index>ALL

出现ALL就是全表扫描, 需要进行优化。一般来说, 得保证查询至少达到range级别, 最好能达到ref。

将where条件用到的字段加上索引

# Extra列

## Using filesort

出现这个选项的常见情况就是 Where 条件和 order by 或 group by 子句作用在了不同的列上

当Where 条件和 order by 或 group by 子句作用在不同的列上, 建立联合索引可以避免Using filesort的产生

比如 select * from a where type = 5 order by id 即使在 type 和 id 上分别添加了索引也不行

解决方法: 在 type, id 两列上建立一个联合索引
