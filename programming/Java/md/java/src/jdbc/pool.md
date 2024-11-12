# 使用 HikariCP 连接池

```java
package com.example;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.*;

public class App {
    public static void main(String[] args) {
        String url = "jdbc:mariadb://127.0.0.1:3306/db_test?characterEncoding=UTF-8&useSSL=false";
        String username = "test";
        String password = "123456";

        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(url);
        config.setUsername(username);
        config.setPassword(password);
        // 缓存PreparedStatement对象
        // 设置为 true 时，数据库连接池会将常用的预编译语句缓存起来，
        // 以便于下次执行相同的 SQL 语句时可以复用，从而减少预编译的时间开销，提高效率
        config.addDataSourceProperty("cachePrepStmts", "true");
        // 预编译语句缓存的最大数量为 250
        config.addDataSourceProperty("prepStmtCacheSize", "250");
        // 单个预编译语句的最大长度限制为 2048 字符
        // 防止过长的 SQL 语句占用过多的缓存资源
        config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");

        // 创建数据库连接池
        try (HikariDataSource ds = new HikariDataSource(config)) {
            // 从连接池中获取数据库连接
            try (Connection connection = ds.getConnection()) {
                String query = "select * from student_info where student_name = ?";
                try (PreparedStatement statement = connection.prepareStatement(query)) {
                    statement.setString(1, "tom");
                    try (ResultSet resultSet = statement.executeQuery()) {
                        while (resultSet.next()) {
                            String studentId = resultSet.getString("student_id");
                            System.out.println(studentId);
                        }
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
```
