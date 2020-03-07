# 步骤：
```java
//1. 导入驱动jar包
//2.注册驱动
Class.forName("com.mysql.jdbc.Driver");
//3.获取数据库连接对象
Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/db3", "uid", "pwd");
//4.定义sql语句
String sql = "update account set balance = 500 where id = 1";
//5.获取执行sql的对象 Statement
Statement stmt = conn.createStatement();
//6.执行sql
int count = stmt.executeUpdate(sql);
//7.处理结果
System.out.println(count);
//8.释放资源
stmt.close();
conn.close();
```
# 管理事务
```java
// 设置参数为false开启事务
conn.setAutoCommit(boolean autoCommit)
// 提交事务
conn.commit()
// 回滚事务
conn.rollback()
```
# Statement执行sql
```java
// 执行非select语句
int executeUpdate(String sql)
// 执行select语句
ResultSet executeQuery(String sql)
```
# ResultSet封装查询结果
```java
// 遍历结果集
// ResultSet rs
while(rs.next()){
    //获取数据
	int id = rs.getInt(1);
	String name = rs.getString("name");
	double balance = rs.getDouble(3);
	// 输出数据
	System.out.println(id);
}
```
# PreparedStatement执行sql解决sql注入问题
```java
String sql ="select * from user where username=?";
PreparedStatement p = conn.prepareStatement(sql);
p.setString(1, "zhangsan");
ResultSet rs = stmt.executeQuery();
```
