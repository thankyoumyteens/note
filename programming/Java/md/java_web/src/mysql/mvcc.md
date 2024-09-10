# MVCC

MVCC 和排他锁确保了事务的隔离性。

MVCC(Multi-Version Concurrency Control, 多版本并发控制)允许多个事务同时对同一数据进行读取和写入操作, 而不会相互干扰。MVCC 不能解决幻读问题。

InnoDB 通过 undo log 保存每条数据的多个版本, 并且能够找回数据历史版本,

MVCC 只在已提交读和可重复读两个隔离级别下工作, 其他两个隔离级别和 MVCC 是不兼容的。因为未提交读总是读取最新的数据, 而不是读取符合当前事务版本的数据行。而串行化不允许事务并发执行。在可重复读中, 每个事务读到的数据版本可能是不一样的, 在同一个事务中, 用户只能看到该事务创建快照之前已经提交的修改和该事务本身做的修改。

事务每次开启时, 都会从数据库获得一个自增长的事务 ID, 可以从事务 ID 判断事务的执行先后顺序, 这个 ID 称为事务版本号。

## 隐藏列

对于 InnoDB 存储引擎, 每一行记录都有两个隐藏列 trx_id 和 roll_pointer, 如果数据表中存在主键或者非 NULL 的 UNIQUE 键时不会创建 row_id, 否则 InnoDB 会自动生成单调递增的隐藏主键 row_id。

- trx_id: 记录操作该行数据事务的事务 ID
- roll_pointer: 回滚指针, 指向当前记录行的 undo log 信息

undo log 分为两类:

1. insert undo log: insert 时产生的 undo log, 只在事务回滚时需要, 并且在事务提交后就可以立即删除
2. update undo log: delete 和 update 时产生的 undo log, 不仅在事务回滚时需要, 快照读也需要, 只有当数据库所使用的快照中不涉及该日志记录, 对应的回滚日志才会被删除

## 版本链

多个事务并行操作某一行数据时, 不同事务对该行数据的修改会产生多个版本, 然后通过回滚指针(roll_pointer), 连成一个链表, 这个链表就称为版本链。

![](../img/tc.png)

快照读: 读取的是记录数据的可见版本(有旧的版本)。不加锁,普通的 select 语句都是快照读

```sql
select * from my_table where id = 1;
```

当前读: 读取的是记录数据的最新版本, 显式加锁的都是当前读

```sql
select * from my_table where id = 1 for update;
select * from my_table where id = 1 lock in share mode;
```

## ReadView

ReadView 是当前事务开启的快照记录。

ReadView 的几个重要属性:

- trx_ids: 当前未提交的事务 ID 集合(不包括当前事务自己和已提交的事务)
- low_limit_id: 目前出现过的最大的事务 ID+1(不管提没提交), 即下一个将被分配的事务 ID。如果最大的事务 id 是 10, 那么 low_limit_id 就是 11
- up_limit_id: trx_ids 中最小的事务 ID, 如果 trx_ids 为空, 则 up_limit_id 为 low_limit_id
- creator_trx_id: 表示生成该 ReadView 的事务的 id

ReadView 的创建时机:

1. read committed 隔离级别下, 每个 select 都会创建最新的 ReadView
2. repeatable read 隔离级别下, 则是当事务中的第一个 select 请求才创建 ReadView

访问某条记录的时候, 确定要访问的版本:

- 如果这条记录的 trx_id == creator_trx_id, 那么表示当前事务访问的是自己修改过的记录, 那么该版本对当前事务可见；
- 如果这条记录的 trx_id < up_limit_id, 那么表示生成该版本的事务在当前事务生成 ReadView 前已经提交, 所以该版本可以被当前事务访问
- 如果这条记录的 trx_id > low_limit_id 值, 那么表示生成该版本的事务在当前事务生成 ReadView 后才开启, 所以该版本不可以被当前事务访问
- 如果这条记录的 trx_id 在 up_limit_id 和 m_low_limit_id 之间, 那就需要判断一下这个 trx_id 是不是在 trx_ids 列表中
  - 如果在, 说明创建 ReadView 时生成该版本的事务还是活跃的, 该版本不可以被访问
  - 如果不在, 说明创建 ReadView 时生成该版本的事务已经被提交, 该版本可以被访问
- 如果最新的数据不符合 ReadView 的可见性规则, 那么就需要去 undo log 中查找历史快照, 直到返回符合规则的数据
