# 基本使用

### 1.依赖

```xml
<dependency>
    <groupId>org.mariadb.jdbc</groupId>
    <artifactId>mariadb-java-client</artifactId>
    <version>3.5.0</version>
</dependency>
```

### 2. 使用

```java
package com.example;

import java.sql.*;

public class App {
    public static void main(String[] args) {
        String url = "jdbc:mariadb://127.0.0.1:3306/db_test?characterEncoding=UTF-8&useSSL=false";
        String username = "test";
        String password = "123456";

        // 连接oracle的话要加上, 否则打包后会找不到驱动
        // Class.forName("oracle.jdbc.driver.OracleDriver");

        // DriverManager会扫描classpath, 找到所有的JDBC驱动, 然后根据传入的URL挑选一个合适的驱动
        try (Connection connection = DriverManager.getConnection(url, username, password)) {
            String query = "select * from student_info where student_name = ?";
            try (PreparedStatement statement = connection.prepareStatement(query)) {
                // 设置参数
                statement.setString(1, "tom");
                // 执行查询语句, 返回结果集
                try (ResultSet resultSet = statement.executeQuery()) {
                    // 遍历结果集
                    while (resultSet.next()) {
                        // 获取指定列的值
                        String studentId = resultSet.getString("student_id");
                        System.out.println(studentId);
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
```
