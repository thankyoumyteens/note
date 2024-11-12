# 批量执行

```java
String query = "insert into student_info(student_name, student_age, student_phone) values(?, ?, ?)";
// 创建PreparedStatement对象
try (PreparedStatement statement = connection.prepareStatement(query)) {
    // 新增10条数据
    for (int i = 0; i < 10; i++) {
        statement.setString(1, "student" + i);
        statement.setInt(2, 10 + i);
        statement.setString(3, "1351234567" + i);
        // 添加到批处理
        statement.addBatch();
    }
    // 执行更新, 返回更新的行数
    int[] effectedRows = statement.executeBatch();
    System.out.println("Effected rows: " + Arrays.toString(effectedRows));
}
```
