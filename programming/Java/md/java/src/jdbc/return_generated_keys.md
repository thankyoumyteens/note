# 新增后获取自增主键

```java
String query = "insert into student_info(student_name, student_age, student_phone) values(?, ?, ?)";
// 创建PreparedStatement对象, RETURN_GENERATED_KEYS表示返回自增的列(自增列不一定必须是主键)
try (PreparedStatement statement = connection.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {
    // 设置参数
    statement.setString(1, "jerry");
    statement.setInt(2, 10);
    statement.setString(3, "13512345678");
    // 执行更新
    int effectedRows = statement.executeUpdate();
    // 如果一次插入多条记录，那么这个ResultSet对象就会有多行返回值
    // 如果插入时有多列自增，那么ResultSet对象的每一行都会对应多个自增值
    ResultSet generatedKeys = statement.getGeneratedKeys();
    // 获取自动生成的主键
    if (generatedKeys.next()) {
        // 索引从1开始
        System.out.println("Generated key: " + generatedKeys.getLong(1));
    }
}
```
