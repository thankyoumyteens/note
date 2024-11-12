# 查询

```java
String query = "select * from student_info where student_name = ?";
// 创建PreparedStatement对象
try (PreparedStatement statement = connection.prepareStatement(query)) {
    // 设置参数
    statement.setString(1, "tom");
    // 执行查询语句，返回结果集
    try (ResultSet resultSet = statement.executeQuery()) {
        // 遍历结果集
        while (resultSet.next()) {
            // 获取指定列的值
            String studentId = resultSet.getString("student_id");
            System.out.println(studentId);
        }
    }
}
```
