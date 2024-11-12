# 更新

```java
String query = "update student_info set student_age = ? where student_name = ?";
// 创建PreparedStatement对象
try (PreparedStatement statement = connection.prepareStatement(query)) {
    // 设置参数
    statement.setInt(1, 10);
    statement.setString(2, "tom");
    // 执行更新, 返回更新的行数
    int effectedRows = statement.executeUpdate();
    System.out.println("Effected rows: " + effectedRows);
}
```
