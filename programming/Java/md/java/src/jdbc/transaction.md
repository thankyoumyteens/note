# 事务

```java
// 设置数据库隔离级别
connection.setTransactionIsolation(Connection.TRANSACTION_REPEATABLE_READ);
try {
    // 关闭自动提交(开启事务)
    connection.setAutoCommit(false);

    insert(connection);
    int a = 1 / 0;
    insert(connection);

    // 提交事务
    connection.commit();
    System.out.println("Commit");
} catch (SQLException e) {
    // 回滚事务
    connection.rollback();
    System.out.println("Rollback");
} finally {
    // 恢复自动提交
    connection.setAutoCommit(true);
}
```
